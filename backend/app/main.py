from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.services.cohere_service import cohere_service
from app.models.schemas import ChatRequest, ChatResponse
from app.api import upload
from app.services.vector_service import vector_service
import logging

# Set up logging
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)

@app.get("/")
async def root():
    return {"message": "AI Voice Bot is running!"}

@app.get("/test-ai")
async def test_ai_endpoint():
    """Test if Cohere is working"""
    success = await cohere_service.test_connection()
    return {"ai_connected": success}

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message with knowledge base context"""
    try:
        # Search for relevant documents
        relevant_docs = await vector_service.search(request.message)
        
        # Combine documents into context
        context = "\n\n".join(relevant_docs) if relevant_docs else None
        
        # Generate response with context
        response_text, tokens_used = await cohere_service.generate_response(
            prompt=request.message,
            context=context
        )
        
        session_id = request.session_id or f"session_{hash(request.message)}"
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            tokens_used=tokens_used
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 