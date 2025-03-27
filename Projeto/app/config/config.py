from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    DATABASE_PORT: int
    POSTGRES_DB: str

    class Config:
        env_file = ".env"  # Caminho do arquivo .env
        env_file_encoding = 'utf-8'

settings = Settings()

