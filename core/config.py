from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_STT_MODEL: str = "whisper-1"
    OPENAI_STT_LANGUAGE: str = "ko"

    OPENAI_LLM_MODEL: str = "gpt-5-mini"

    KAKAO_REST_API_KEY: str = Field(default="", description="Kakao REST API Key for Local API")
    KAKAO_LOCAL_BASE_URL: str = "https://dapi.kakao.com"
    HTTP_TIMEOUT_SEC: float = 3.0

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

settings = Settings()
