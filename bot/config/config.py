from dataclasses import dataclass
from environs import Env


@dataclass
class DbPostgresConfig:
    db_name: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class Bot:
    token: str


@dataclass
class Config:
    bot: Bot
    dbPostgres: DbPostgresConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(bot=Bot(token=env('HTTP_API_BOT_TOKEN')),
                  dbPostgres=DbPostgresConfig(db_name=env('DB_NAME'),
                                              db_host=env('DB_HOST'),
                                              db_user=env('DB_USER'),
                                              db_password=env('DB_PASSWORD')))
