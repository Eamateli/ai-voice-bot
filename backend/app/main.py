from fastapi import FastAPI
from app.services.cohere_service import test_cohere, chat_with_ai
from app.models.schemas import ChatRequest, ChatResponse
from app.api import upload
from app.services.vector_service import vector_service

app= FastAPI()
app.include_router(upload.router)


@app.get("/")
async def root():
    return {"message":"AI Voice Bot is running!"}


@app.get("/test-ai")
async def test_ai_endpoint():
    ai_response = test_cohere()
    return {"ai_says": ai_response}


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    relevant_docs = await vector_service.search(request.message)
    if relevant_docs:
        context = "\n\n".join(relevant_docs)
        ai_response, tokens = chat_with_ai(request.message, context)
    else:
        ai_response, tokens = chat_with_ai(request.message)
    
    return ChatResponse (
        response=ai_response,
        tokens_used= tokens
    ) 

