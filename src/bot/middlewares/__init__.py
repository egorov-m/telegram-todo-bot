from aiogram import BaseMiddleware

from bot.middlewares.database import DatabaseMiddleware
from bot.middlewares.translator import TranslatorMiddleware
from bot.middlewares.user import ActiveUserMiddleware, ProtectionUserMiddleware

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
