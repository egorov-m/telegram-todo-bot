from aiogram import BaseMiddleware

from src.bot.middlewares.database import DatabaseMiddleware
from src.bot.middlewares.translator import TranslatorMiddleware
from src.bot.middlewares.user import ActiveUserMiddleware, ProtectionUserMiddleware

middlewares: list[BaseMiddleware] = [
    DatabaseMiddleware(),
    ActiveUserMiddleware(),
    TranslatorMiddleware(),
    ProtectionUserMiddleware()
]

__all__ = [
    "DatabaseMiddleware",
    "ActiveUserMiddleware",
    "TranslatorMiddleware",
    "ProtectionUserMiddleware",
    "middlewares"
]
