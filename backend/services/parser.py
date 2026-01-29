# backend/services/parser.py
import fitz
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Create executor for CPU-bound work
_executor = ThreadPoolExecutor(max_workers=2)

def _extract_sync(file_bytes):
    """Synchronous PDF extraction"""
    pages_text = []
    with fitz.open(stream=file_bytes, filetype='pdf') as doc:
        for page in doc:
            pages_text.append(page.get_text())
    return "\n".join(pages_text).strip()

async def extract_text_from_pdf(file_bytes):
    """Async wrapper for PDF extraction"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _extract_sync, file_bytes)