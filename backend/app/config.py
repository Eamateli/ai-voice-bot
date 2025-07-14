from  pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cohere_api_key: str

    class Confing:
        env_file = ".env"


settings = Settings()


