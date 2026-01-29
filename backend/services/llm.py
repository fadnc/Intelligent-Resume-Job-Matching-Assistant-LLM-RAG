# backend/services/llm.py
import json
import re
from transformers import pipeline, AutoTokenizer
from backend.config import USE_SAGEMAKER

# Load tokenizer to check length
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=256,
    tokenizer=tokenizer,
    truncation=True  # Add this - ensures pipeline truncates
)

def truncate_prompt(prompt: str, max_length: int = 400):
    """
    Truncate prompt to fit model's context window.
    T5 has 512 token limit, so 400 input + 112 output is safe
    """
    tokens = tokenizer.encode(prompt, add_special_tokens=True, truncation=True, max_length=max_length)
    prompt = tokenizer.decode(tokens, skip_special_tokens=True)
    print(f"[DEBUG] Truncated prompt to {len(tokens)} tokens")
    return prompt

def extract_json(text: str):
    """
    Safely extract JSON object from model output.
    """
    text = text.strip()
    
    # Try multiple JSON extraction strategies
    
    # Strategy 1: Find complete JSON object with nested braces
    match = re.search(r'\{(?:[^{}]|\{[^{}]*\})*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    # Strategy 2: Find simple JSON object (no nested braces)
    match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: Try to parse the entire text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    raise ValueError(f"No valid JSON found in output: {text[:200]}")

def parse_flan_output(output: str):
    """
    Parse Flan-T5 output which often returns partial or malformed JSON.
    """
    try:
        return extract_json(output)
    except ValueError:
        result = {
            "score": 0,
            "missing_skills": [],
            "suggestions": [],
            "rewritten_bullets": []
        }
        
        # Try to extract score
        score_match = re.search(r'"?score"?\s*:\s*(\d+)', output)
        if score_match:
            result["score"] = int(score_match.group(1))
        
        # Try to extract arrays
        skills_match = re.search(r'"?missing_skills"?\s*:\s*\[(.*?)\]', output, re.DOTALL)
        if skills_match:
            items = re.findall(r'"([^"]+)"', skills_match.group(1))
            result["missing_skills"] = items
        
        suggestions_match = re.search(r'"?suggestions"?\s*:\s*\[(.*?)\]', output, re.DOTALL)
        if suggestions_match:
            items = re.findall(r'"([^"]+)"', suggestions_match.group(1))
            result["suggestions"] = items
        
        bullets_match = re.search(r'"?rewritten_bullets"?\s*:\s*\[(.*?)\]', output, re.DOTALL)
        if bullets_match:
            items = re.findall(r'"([^"]+)"', bullets_match.group(1))
            result["rewritten_bullets"] = items
        
        return result

def call_local_llm(prompt: str):
    """
    Call local Flan-T5 model with truncation and robust parsing.
    """
    # CRITICAL: Truncate BEFORE passing to model
    truncated = truncate_prompt(prompt, max_length=400)
    
    print(f"[DEBUG] Prompt length after truncation: {len(truncated)} chars")
    print(f"[DEBUG] Truncated prompt preview: {truncated[:200]}...")
    
    # Generate output with explicit truncation parameters
    output = generator(
        truncated,
        max_length=512,  # Total tokens (input + output)
        truncation=True
    )[0]["generated_text"]
    
    print(f"[DEBUG] LLM Raw Output: {output}")
    
    try:
        result = parse_flan_output(output)
        print(f"[DEBUG] Parsed Result: {result}")
        return result
        
    except Exception as e:
        print(f"[ERROR] Parse Error: {e}")
        print(f"[ERROR] Full Output: {output}")
        
        return {
            "score": 0,
            "missing_skills": ["Unable to parse model output"],
            "suggestions": [
                "The AI model produced invalid output.",
                "Try using a shorter resume or job description.",
                "Consider upgrading to a larger model (Flan-T5-large or GPT)."
            ],
            "rewritten_bullets": []
        }

def call_llm(prompt):
    if USE_SAGEMAKER:
        raise NotImplementedError("SageMaker integration not yet implemented")
    else:
        return call_local_llm(prompt)