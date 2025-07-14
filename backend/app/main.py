from fastapi import FastAPI
from app.services.cohere_service import test_cohere

app= FastAPI()

@app.get("/")
async def root():
    return {"message":"AI Voice Bot is running!"}

@app.get("/test-ai")
async def test_ai_endpoint():
    ai_response = test_cohere()
    return {"ai_says": ai_response}