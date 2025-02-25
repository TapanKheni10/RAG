from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = "/Users/tapankheni/Desktop/RAG/src/.env",
        extra = "ignore"
    )

    COHERE_API_KEY: str
    PINECONE_API_KEY: str
    GROQ_API_KEY: str
    COHERE_API_KEY: str

Config = Settings()