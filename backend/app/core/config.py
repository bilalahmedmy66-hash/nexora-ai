from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BACKEND_DIR.parent

INSECURE_DEFAULTS = {
    "change-me-to-a-long-random-string",
    "change-me-too",
    "dev-insecure-secret",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env", BACKEND_DIR / ".env"),
        extra="ignore",
    )

    app_env: str = "development"
    app_name: str = "Nexora AI"
    app_secret_key: str = "dev-insecure-secret"
    database_url: str = f"sqlite:///{BACKEND_DIR / 'nexora.db'}"
    jwt_secret: str = "dev-insecure-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    cors_allowed_origins: str = "http://localhost:5173"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    def validate_for_runtime(self) -> None:
        if self.is_production and (self.jwt_secret in INSECURE_DEFAULTS or len(self.jwt_secret) < 32):
            raise RuntimeError("JWT_SECRET must be a random string of 32+ characters in production.")


@lru_cache
def get_settings() -> Settings:
    return Settings()
