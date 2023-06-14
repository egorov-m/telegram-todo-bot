from src.bot.structures.data_structure import BotItem, BotItem

from aiogram.filters.callback_data import CallbackData


class MainCallback(CallbackData, prefix=BotItem.MAIN):
    pass


class AddTaskCallback(CallbackData, prefix=BotItem.ADD_TASK):
    pass


class DeleteTaskCallback(CallbackData, prefix=BotItem.DELETE_TASK):
    pass


class DoneTaskCallback(CallbackData, prefix=BotItem.DONE_TASK):
    pass


class EditTaskCallback(CallbackData, prefix=BotItem.EDIT_TASK):
    pass


class UpdateListCallback(CallbackData, prefix=BotItem.UPDATE_LIST):
    pass


class SettingsCallback(CallbackData, prefix=BotItem.SETTINGS):
    pass


class BackCallback(CallbackData, prefix=BotItem.BACK):
    where_from: str = BotItem.MAIN


class LanguagesCallback(CallbackData, prefix=BotItem.SETTINGS_LANGUAGES):
    """
    Callback - Bot language settings section
    """
    pass


class LanguageCallback(CallbackData, prefix=BotItem.LANGUAGE):
    """
    Callback - language selected
    """
    language: str
