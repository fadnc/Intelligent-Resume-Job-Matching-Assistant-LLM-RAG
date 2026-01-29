# backend/services/llm.py
import json
import re
import os
from backend.config import USE_SAGEMAKER, GROQ_API_KEY, USE_GROQ

def call_groq_llm(prompt: str):
    """Call Groq API for fast, reliable JSON generation"""
    from groq import Groq
    
    client = Groq(api_key=GROQ_API_KEY)
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Fast and accurate
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert resume analyzer and ATS evaluator. 
You MUST respond with ONLY valid JSON in the exact format specified. 
No additional text, explanations, or markdown - just pure JSON."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=800,
            response_format={"type": "json_object"}  # Force JSON output
        )
        
        output = response.choices[0].message.content
        print(f"[DEBUG] Groq Output: {output[:200]}...")
        
        # Parse JSON
        result = json.loads(output)
        
        # Validate structure
        required_keys = ["score", "missing_skills", "suggestions", "rewritten_bullets"]
        if all(key in result for key in required_keys):
            print(f"[DEBUG] Successfully parsed result with score: {result.get('score')}")
            return result
        else:
            print(f"[WARNING] Missing required keys in response")
            return {
                "score": result.get("score", 0),
                "missing_skills": result.get("missing_skills", []),
                "suggestions": result.get("suggestions", ["Incomplete response from AI"]),
                "rewritten_bullets": result.get("rewritten_bullets", [])
            }
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON Parse Error: {e}")
        print(f"[ERROR] Raw output: {output}")
        return {
            "score": 0,
            "missing_skills": [],
            "suggestions": ["AI generated invalid JSON response"],
            "rewritten_bullets": []
        }
    except Exception as e:
        print(f"[ERROR] Groq API Error: {e}")
        return {
            "score": 0,
            "missing_skills": [],
            "suggestions": [f"API Error: {str(e)[:100]}"],
            "rewritten_bullets": []
        }

def call_local_llm(prompt: str):
    """Fallback local model (kept for compatibility)"""
    print("[WARNING] Using fallback local model - install Groq for better results")
    return {
        "score": 0,
        "missing_skills": ["Groq API key not configured"],
        "suggestions": [
            "Add GROQ_API_KEY to your .env file",
            "Get free API key from https://console.groq.com/keys"
        ],
        "rewritten_bullets": []
    }

def call_llm(prompt: str):
    """Main LLM dispatcher"""
    if USE_SAGEMAKER:
        raise NotImplementedError("SageMaker integration not yet implemented")
    elif USE_GROQ:
        return call_groq_llm(prompt)
    else:
        return call_local_llm(prompt)