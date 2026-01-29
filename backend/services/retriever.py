import faiss
import hashlib

_INDEX_CACHE = {}


def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()


def create_index(vectors, chunks, resume_text):
    key = hash_text(resume_text)

    # if already cached
    if key in _INDEX_CACHE:
        return key

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    # IMPORTANT: store in cache
    _INDEX_CACHE[key] = (index, chunks)

    return key   # IMPORTANT: must return


def search(query_vec, key, k=5):
    index, chunks = _INDEX_CACHE[key]

    distances, indices = index.search(query_vec.reshape(1, -1), k)

    return [chunks[i] for i in indices[0]]
