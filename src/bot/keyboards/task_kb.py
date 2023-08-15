from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.callback_factories import (
    CancelCallback,
    DeleteSelectedTasksCallback,
    DeleteAllTasksCallback,
    SelectTaskDeleteCallback,
    DoneStateAllTasksCallback,
    DoneStateNothingTasksCallback,
    SaveDoneStateTaskCallback,
    ChangeDoneStateTaskCallback,
    AddTaskSaveCallback,
    BackCallback,
    SelectTaskForEditCallback,
    SaveEditTaskCallback,
    EditTaskTitleCallback,
    EditTaskDescriptionCallback
)
from src.bot.states.data import DeletableTask, DoneTask, AddTaskStateData
from src.bot.structures.data_structure import BotBtnTitle, BotItem
from src.bot.utils.html.message_template import deletion_marker, done_marker
from src.db.models import Task
from src.lexicon import Translator


async def create_add_task_keyboard(translator: Translator,
                                   task_data=None,
                                   where_from: BotItem = BotItem.MAIN, isSave: bool = False) -> InlineKeyboardMarkup:
    if task_data is None:
        task_data = {}
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: [InlineKeyboardButton] = [InlineKeyboardButton(text=await translator.translate(BotBtnTitle.CANCEL),
                                                            callback_data=CancelCallback().pack())]
    if isSave and task_data is not None:
        buttons.append(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.SAVE),
                                            callback_data=AddTaskSaveCallback(
                                                task_title=task_data.get(AddTaskStateData.TASK_TITLE),
                                                task_description=task_data.get(AddTaskStateData.TASK_DESCRIPTION))
                                            .pack()))
    buttons.append(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                        callback_data=BackCallback(where_from=where_from).pack()))
    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()


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


async def create_edit_task_select_task_keyboard(translator: Translator, tasks: list[Task]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.CANCEL),
                                        callback_data=CancelCallback().pack()),
                   *[InlineKeyboardButton(text=f"{done_marker(task.is_done)} {task.title}",
                                          callback_data=SelectTaskForEditCallback(
                                              task_id=str(task.id)
                                          ).pack()) for task in tasks], width=1)

    return kb_builder.as_markup()


async def create_edit_task_select_edit_item_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate(BotBtnTitle.CANCEL),
                                          callback_data=CancelCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.SAVE),
                                          callback_data=SaveEditTaskCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.CHANGE_TITLE),
                                          callback_data=EditTaskTitleCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.CHANGE_DESCRIPTION),
                                          callback_data=EditTaskDescriptionCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                          callback_data=BackCallback(where_from=BotItem.EDIT_TASK).pack())], width=2)

    return kb_builder.as_markup()
