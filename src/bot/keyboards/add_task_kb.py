from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot.states.data import AddTaskStateData
from src.bot.keyboards.callback_factories import BackCallback, CancelCallback, AddTaskSaveCallback
from src.bot.structures.data_structure import BotBtnTitle, BotItem
from src.lexicon.translator import Translator


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
