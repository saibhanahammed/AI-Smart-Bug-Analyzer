def generate_text_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """Splits a single log text body into overlapping context windows."""
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
        
    return chunks