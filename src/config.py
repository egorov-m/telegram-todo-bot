"""This file represents configurations from files and environment"""
from dataclasses import dataclass
from environs import Env


@dataclass
class DbPostgresConfig:
    """Postgres database connection variables"""

    db_name: str
    db_host: str
    db_port: str
    db_user: str
    db_password: str

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def get_url(self) -> str:
        return f"{self.database_system}+{self.driver}://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"


@dataclass
class DbRedisConfig:
    """Redis connection variables"""

    db_name: str
    db_host: str
    db_port: str
    db_user: str
    db_password: str


@dataclass
class Bot:
    """Bot configuration"""

    token: str


@dataclass
class Config:
    """All in one configuration's class"""

    bot: Bot
    dbPostgres: DbPostgresConfig
    dbRedis: DbRedisConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(bot=Bot(token=env('HTTP_API_BOT_TOKEN')),
                  dbPostgres=DbPostgresConfig(db_name=env('POSTGRES_DB_NAME'),
                                              db_host=env('POSTGRES_DB_HOST'),
                                              db_port=env('POSTGRES_DB_PORT'),
                                              db_user=env('POSTGRES_DB_USER'),
                                              db_password=env('POSTGRES_DB_PASSWORD')),
                  dbRedis=DbRedisConfig(db_name=env('REDIS_DB_NAME'),
                                        db_host=env('REDIS_DB_HOST'),
                                        db_port=env('REDIS_DB_PORT'),
                                        db_user=env('REDIS_DB_USER'),
                                        db_password=env('REDIS_DB_PASSWORD')))
