"""This file represents configurations from files and environment"""

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Telegram ToDo Bot"

    TELEGRAM_API_BOT_TOKEN: str = "token"

    LIMIT_USERS_ON_PAGE: int = 5
    COUNT_LIMITS_TASKS_STORAGE_USER = 20

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "secret"
    POSTGRES_DB: str = "postgres"

    POSTGRES_DATABASE_SYSTEM: str = "postgresql"
    POSTGRES_DRIVER: str = "asyncpg"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_DB: str = "0"

    def get_postgres_url(self):
        return f"{self.POSTGRES_DATABASE_SYSTEM}+{self.POSTGRES_DRIVER}://" \
               f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@" \
               f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
