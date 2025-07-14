from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str 


class ChatRespose(BaseModel):
    response: str
    tokens_used: int
