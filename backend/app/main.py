from fastapi import FastAPI
from app.services.cohere_service import test_cohere
from app.models.schemas import ChatRequest, ChatRespose

app= FastAPI()

@app.get("/")
async def root():
    return {"message":"AI Voice Bot is running!"}

@app.get("/test-ai")
async def test_ai_endpoint():
    ai_response = test_cohere()
    return {"ai_says": ai_response}

@app.post("/api/v1/chat", response_model=ChatRespose)
async def chat(request: ChatRequest):
    return ChatRespose (
        response=f"You said: {request.message}",
        token_used=10
    ) 