from transformers import pipeline

generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")

def predict_fn(data, model):
    prompt = data["prompt"]
    output = generator(prompt)[0]["generated_text"]
    return output
