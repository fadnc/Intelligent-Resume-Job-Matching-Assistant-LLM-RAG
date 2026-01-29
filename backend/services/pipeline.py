from services.parser import extract_text_from_pdf
from services.chunker import chunk_text
from services.llm import call_llm
from services.embeddings import embed_texts
from models.prompts import PROMPT_TEMPLATE
from services.retriever import create_index, search

async def analyze_resume(resume_file, job_text):
    file_bytes = await resume_file.read()
    
    #s1 parse
    resume_text = extract_text_from_pdf(file_bytes)
    
    #s2 chunk
    chunks = chunk_text(resume_text)
    
    #s3 embed & index
    vectors = embed_texts(chunks)
    cache_key = create_index(vectors, chunks, resume_text)
    
    #s4 retrieve relev chunks
    query_vec = embed_texts([job_text])[0]
    top_chunks = search(query_vec, cache_key)
    
    context = "\n".join(top_chunks)
    
    #s5 llm prompt
    prompt = PROMPT_TEMPLATE.format(
        resume=context,
        jd=job_text
    )
    
    #s6 call llm
    result = call_llm
    
    return result
    