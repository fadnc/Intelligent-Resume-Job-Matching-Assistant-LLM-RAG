from backend.services.parser import extract_text_from_pdf
from backend.services.chunker import chunk_text
from backend.services.embeddings import embed_texts
from backend.services.retriever import create_index, search
from backend.services.llm import call_llm
from backend.models.prompts import PROMPT_TEMPLATE
from functools import lru_cache

@lru_cache(maxsize=100)
def get_jd_embedding(job_text):
    return embed_texts([job_text])[0]


async def analyze_resume(resume_file, job_text):
    file_bytes = await resume_file.read()
    
    resume_text =await  extract_text_from_pdf(file_bytes)
    
    chunks = chunk_text(resume_text)
    
    vectors = embed_texts(chunks)
    cache_key = create_index(vectors, chunks, resume_text)
    
    query_vec = get_jd_embedding(job_text)
    top_chunks = search(query_vec, cache_key)
    
    context = "\n".join(top_chunks)
    
    prompt = PROMPT_TEMPLATE.format(
        resume=context,
        jd=job_text
    )
    
    result = call_llm(prompt)
    
    return result
    