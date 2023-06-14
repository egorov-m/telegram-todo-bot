from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.db.models.task import Task


def create_delete_tasks_keyboard(tasks: List[Task], isInProcess: bool = False) -> InlineKeyboardMarkup:
    pass


def create_edit_task_keyboard(isInProcess: bool = False) -> InlineKeyboardMarkup:
    pass
