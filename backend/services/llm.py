import json
import re
from transformers import pipeline
from backend.config import USE_SAGEMAKER


generator = pipeline(
    "text2text-generation",   # FIXED for T5
    model="google/flan-t5-base",
    max_new_tokens=128
    # temperature=0.2,
    # do_sample=False
)


def extract_json(text: str):
    """
    Safely extract first JSON object from model output
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No JSON found")


def call_local_llm(prompt: str):
    output = generator(prompt)[0]["generated_text"].replace(prompt, "")

    try:
        return extract_json(output)

    except Exception:
        return {
            "score": 0,
            "missing_skills": [],
            "suggestions": ["LLM parsing failed"],
            "rewritten_bullets": []
        }


def call_llm(prompt):
    if USE_SAGEMAKER:
        pass
    else:
        return call_local_llm(prompt)
