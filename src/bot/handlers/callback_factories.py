from aiogram.filters.callback_data import CallbackData


class AddTaskCallback(CallbackData, prefix='add_task'):
    action: str = None
    entity_id: int = None
    message_ids: str = None


class DeleteTaskCallback(CallbackData, prefix='delete_task'):
    action: str
    entity_id: int
    message_ids: str


class EditTaskCallback(CallbackData, prefix='edit_task'):
    action: str
    entity_id: int
    message_ids: str
