from src.bot.structures.data_structure import BotPages, BotButtons

from aiogram.filters.callback_data import CallbackData


class MainCallback(CallbackData, prefix=BotButtons.MAIN):
    pass


class AddTaskCallback(CallbackData, prefix=BotButtons.ADD_TASK):
    pass


class DeleteTaskCallback(CallbackData, prefix=BotButtons.DELETE_TASK):
    pass


class DoneTaskCallback(CallbackData, prefix=BotButtons.DONE_TASK):
    pass


class EditTaskCallback(CallbackData, prefix=BotButtons.EDIT_TASK):
    pass


class UpdateListCallback(CallbackData, prefix=BotButtons.UPDATE_LIST):
    pass


class SettingsCallback(CallbackData, prefix=BotButtons.SETTINGS):
    pass


class BackCallback(CallbackData, prefix=BotButtons.BACK):
    where_from: str = BotPages.MAIN


class LanguagesCallback(CallbackData, prefix=BotButtons.SETTINGS_LANGUAGES):
    """
    Callback - Bot language settings section
    """
    pass


class LanguageCallback(CallbackData, prefix=BotButtons.LANGUAGE):
    """
    Callback - language selected
    """
    language: str
