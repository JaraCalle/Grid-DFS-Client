from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NAMENODE_URL: str = "http://127.0.0.1:8000/api/v1/namenode"
    AUTH_TOKEN: str = ""
    BLOCK_SIZE: int = 64 * 1024 * 1024  # 64 MB por defecto

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
