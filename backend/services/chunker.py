def chunk_text(text, size=300, overlap=50):

    if overlap >= size:
        raise ValueError("Overlap must be smaller than size.")

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += size - overlap

    return chunks
