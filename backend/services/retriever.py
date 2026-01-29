import faiss
import hashlib
import numpy as np
from config import FAISS_PATH, META_PATH

_INDEX_CACHE = {}

def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()

def create_index(vectors, chunks, resume_text):
    key = hash_text(resume_text)
    if key in _INDEX_CACHE:
        return key
    
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    
    faiss.write_index(index, FAISS_PATH)
    np.save(META_PATH, np.array(chunks, dtype=object))
    
def search(query_vec, key, k=5):
    index, chunks = _INDEX_CACHE[key]
    
    # index = faiss.read_index(FAISS_PATH)
    # chunks = np.load(META_PATH, allow_pickle=True)
    
    distances, indices = index.search(np.array([query_vec]), k)
    
    return [chunks[i] for i in indices[0]]