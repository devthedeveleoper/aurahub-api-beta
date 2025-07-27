from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Loads and validates application settings from environment variables.
    """
    STREAMTAPE_API_LOGIN: str
    STREAMTAPE_API_KEY: str
    STREAMTAPE_BASE_URL: str = "https://api.streamtape.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()