from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_ECHO_LOG: bool = False
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env"

settings = Settings()