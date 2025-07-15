"""File upload endpoint for documents"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vector_service import vector_service
from app.utils.document_processor import extract_text_from_file, chunk_text
from app.models.schemas import DocumentUpload
import os
import aiofiles

# Create router with prefix and tags
router = APIRouter(prefix="/api/v1", tags=["documents"])

@router.post("/upload", response_model=DocumentUpload)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document to the knowledge base
    
    Args:
        file: The uploaded file (PDF or TXT)
    
    Returns:
        DocumentUpload response with status
    """
    # Check file type
    if not file.filename.endswith(('.txt', '.pdf')):
        raise HTTPException(
            status_code=400, 
            detail="Only .txt and .pdf files are supported"
        )
    
    # Create upload directory if it doesn't exist
    os.makedirs("./data/knowledge_base", exist_ok=True)
    
    # Save file temporarily
    file_path = f"./data/knowledge_base/{file.filename}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    try:
        # Extract text from file
        text = await extract_text_from_file(file_path)
        
        # Split into chunks
        chunks = chunk_text(text)
        
        # Store each chunk in vector DB
        for chunk in chunks:
            await vector_service.add_document(
                chunk,
                metadata={"filename": file.filename}
            )
        
        return DocumentUpload(
            filename=file.filename,
            chunks_created=len(chunks),
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)