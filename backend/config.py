# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

USE_SAGEMAKER = os.getenv("USE_SAGEMAKER", "False").lower() == "true"
SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT", "")

# Groq API settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USE_GROQ = bool(GROQ_API_KEY) and not USE_SAGEMAKER

FAISS_PATH = "embeddings_store/faiss_index"
META_PATH = "embeddings_store/meta.npy"