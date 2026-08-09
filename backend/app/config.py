from  pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

class Settings(BaseSettings):
    COHERE_API_KEY: str
    COHERE_MODEL: str = "command-a-03-2025"  # "command" was retired; this replaces it

    # ElevenLabs (text-to-speech). Without a key the bot falls back to gTTS.
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = "EXAVITQu4vr4xnSDxMaL"  # "Sarah" - usable on the free tier
    ELEVENLABS_MODEL_ID: str = "eleven_flash_v2_5"     # lowest latency, good for real-time

    environment: str = "development"
    cors_origins: List[str] = ["http://localhost:3000"]
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
