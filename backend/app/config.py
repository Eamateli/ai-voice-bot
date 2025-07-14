from  pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    COHERE_API_KEY: str

    class Confing:
        env_file = ".env"


settings = Settings()


