from transformers import pipeline


def model_fn(model_dir):
    generator = pipeline(
        "text-generation",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_new_tokens=500,
        temperature=0.3,
        do_sample=True
    )
    return generator


def predict_fn(data, model):
    prompt = data["prompt"]

    output = model(prompt)[0]["generated_text"]

    return {
        "generated_text": output
    }
