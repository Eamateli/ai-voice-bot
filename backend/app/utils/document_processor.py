"""Document processor for handling PDF and text file uploads."""
import os
from typing import List
from pypdf import PdfReader

async def extract_text_from_file(file_path: str) -> str:
    """Extract text from uploaded file"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    elif file_extension == '.pdf':
        reader = PdfReader(file_path)
        text_parts = []
        
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text.strip(): 
                    text_parts.append(page_text)
            except Exception as e:
                print(f"Error reading page {page_num}: {e}")
                continue
        
        return "\n\n".join(text_parts)
    
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into smaller chunks"""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            current_chunk += "\n\n" + paragraph
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks