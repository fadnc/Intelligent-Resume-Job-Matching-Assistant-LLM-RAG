from sentence_transformers import SentenceTransformer
import numpy as np
import torch
from backend.config import EMBED_MODEL

#use cuda if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(EMBED_MODEL, device=device)

def embed_texts(texts):
    vectors = model.encode(texts, 
                           convert_to_numpy=True,
                           show_progress_bar=False,
                           batch_size=64,
                           normalize_embeddings=True)
    return np.array(vectors).astype("float32")    # imp as vector db expects float32 , if not float64 is slower and eats memory