from sentence_transformers import SentenceTransformer
import numpy as np
from config import EMBED_MODEL

model = SentenceTransformer(EMBED_MODEL)

def embed_texts(texts):
    vectors = model.encode(texts, 
                           convert_to_numpy=True,
                           show_progress_bar=True,
                           batch_size=32)
    return np.array(vectors).astype("float32")    # imp as vector db expects float32 , if not float64 is slower and eats memory