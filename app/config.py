from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "change-this-in-production"
    database_url: str = "sqlite:///./pocketsmart.db"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    access_token_expire_minutes: int = 1440
    max_image_mb: int = 5
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
