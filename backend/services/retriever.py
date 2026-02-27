import faiss
import hashlib
import threading

_INDEX_CACHE = {}
_lock = threading.Lock()

def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()

def create_index(vectors, chunks, resume_text):
    key = hash_text(resume_text)

    with _lock:
        if key in _INDEX_CACHE:
            return key

        dim = vectors.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(vectors)

        _INDEX_CACHE[key] = (index, chunks)

    return key

def search(query_vec, key, k=5):
    index, chunks = _INDEX_CACHE[key]
    distances, indices = index.search(query_vec.reshape(1, -1), k)
    return [chunks[i] for i in indices[0]]