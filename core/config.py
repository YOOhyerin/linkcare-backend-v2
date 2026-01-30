from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    OPENAI_API_KEY: str
    OPENAI_STT_MODEL: str = "whisper-1"
    OPENAI_STT_LANGUAGE: str = "ko"

    OPENAI_LLM_MODEL: str = "gpt-5-mini"


settings = Settings()