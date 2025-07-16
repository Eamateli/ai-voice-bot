from  pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

class Settings(BaseSettings):
    COHERE_API_KEY: str
    environment: str = "development"
    cors_origins: List[str] = ["http://localhost:3000"] 
    api_v1_prefix: str = "/api/v1" 

    class Config:
        env_file = ".env"


settings = Settings()


