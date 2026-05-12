from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import (
    DEFAULT_API_PREFIX,
    DEFAULT_PASSKEY_LENGTH,
    DEFAULT_PASSKEY_MAX_RETRIES,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Smart Parking System"
    app_env: str = "development"
    app_debug: bool = False
    api_prefix: str = DEFAULT_API_PREFIX
    database_url: str = "sqlite:///./parking.db"
    passkey_length: int = Field(default=DEFAULT_PASSKEY_LENGTH, ge=4, le=8)
    passkey_max_retries: int = Field(default=DEFAULT_PASSKEY_MAX_RETRIES, ge=1, le=1000)


settings = Settings()
