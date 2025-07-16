from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str 


class ChatResponse(BaseModel):
    response: str
    tokens_used: int


class DocumentUpload(BaseModel):
    filename: str
    chunks_created: int
    status: str ="success"