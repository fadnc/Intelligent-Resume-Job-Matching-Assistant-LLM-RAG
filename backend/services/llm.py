import json
from transformers import pipeline
from backend.config import USE_SAGEMAKER

generator = pipeline(
    "text-generation",
    #model="mistralai/Mistral-7B-Instruct-v0.2",    #large size approx 14gigs
    model="google/flan-t5-small",    
    max_new_tokens=256
)

def call_local_llm(prompt: str):
    output = generator(prompt)[0]["generated_text"]

    try:
        json_part = output.split("{",1)[1]
        json_part = "{" + json_part
        return json.loads(json_part)
    except:
        return {
            "score": 0,
            "missing_skills": [],
            "suggestions": ["LLM parsing failed"],
            "rewritten_bullets": []
        }

def call_llm(prompt):
    if USE_SAGEMAKER:
        #upgrade later using sagemaker
        #call_sagemaker_llm(prompt)
        pass
    else:
        return call_local_llm(prompt)
