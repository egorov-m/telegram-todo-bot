from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.models.task import Task
import lexicon as lx


def create_delete_tasks_keyboard(tasks: List[Task], isInProcess: bool = False) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row([InlineKeyboardButton(text=task.title, callback_data='delete_task_' + task.id)
                    for task in tasks])
    lexicon: lx.LEXICON = lx.LEXICON_EN()
    kb_builder.row(InlineKeyboardButton(text=lexicon.delete_all_button.text,
                                        callback_data=lexicon.delete_all_button.data))
    btnList: List[InlineKeyboardButton] = []
    if isInProcess:
        btnList.append(InlineKeyboardButton(text=lexicon.save_delete_tasks_button.text,
                                            callback_data=lexicon.save_delete_tasks_button.data))
    btnList.append(InlineKeyboardButton(text=lexicon.cancel_button.text,
                                        callback_data=lexicon.cancel_button.data))
    kb_builder.row(btnList, width=2)

    return kb_builder.as_markup()


def create_edit_task_keyboard(isInProcess: bool = False) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btnList: List[InlineKeyboardButton] = []
    lexicon: lx.LEXICON = lx.LEXICON_EN()
    if isInProcess:
        btnList.append(InlineKeyboardButton(text=lexicon.save_edit_task_button.text,
                                            callback_data=lexicon.save_edit_task_button.data))
    btnList.append(InlineKeyboardButton(text=lexicon.cancel_button.text,
                                        callback_data=lexicon.cancel_button.data))
    kb_builder.row(btnList, width=2)

    return kb_builder.as_markup()
