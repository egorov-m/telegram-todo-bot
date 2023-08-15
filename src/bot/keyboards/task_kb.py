from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.callback_factories import (
    CancelCallback,
    DeleteSelectedTasksCallback,
    DeleteAllTasksCallback,
    SelectTaskDeleteCallback,
    DoneStateAllTasksCallback,
    DoneStateNothingTasksCallback,
    SaveDoneStateTaskCallback,
    ChangeDoneStateTaskCallback
)
from bot.states.data import DeletableTask, DoneTask
from bot.structures.data_structure import BotBtnTitle
from bot.utils.html.message_template import deletion_marker, done_marker
from lexicon import Translator


async def create_delete_task_keyboard(translator: Translator, tasks: list[DeletableTask]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate(BotBtnTitle.CANCEL),
                                          callback_data=CancelCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.DELETE_SELECTED_TASKS),
                                          callback_data=DeleteSelectedTasksCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.DELETE_ALL_TASKS),
                                          callback_data=DeleteAllTasksCallback().pack())], width=2)
    kb_builder.row(*[InlineKeyboardButton(text=f"{deletion_marker(task['is_delete'])} "
                                               f"{done_marker(task['is_done'])} "
                                               f"{task['title']}",
                                          callback_data=SelectTaskDeleteCallback(
                                              task_id=task["task_id"]
                                          ).pack()) for task in tasks], width=1)

    return kb_builder.as_markup()


async def create_done_task_keyboard(translator: Translator, tasks: list[DoneTask]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate(BotBtnTitle.CANCEL),
                                          callback_data=CancelCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.SAVE),
                                          callback_data=SaveDoneStateTaskCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.ALL_DONE_TASK),
                                          callback_data=DoneStateAllTasksCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.NOTHING_DONE_TASK),
                                          callback_data=DoneStateNothingTasksCallback().pack())], width=2)
    kb_builder.row(*[InlineKeyboardButton(text=f"{done_marker(task['is_done'])} "
                                               f"{task['title']}",
                                          callback_data=ChangeDoneStateTaskCallback(
                                              task_id=task["task_id"]
                                          ).pack()) for task in tasks], width=1)

    return kb_builder.as_markup()
