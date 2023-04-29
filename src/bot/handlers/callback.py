from aiogram import types, Router

from src.bot.handlers.callback_factories import AddTaskCallback, DeleteTaskCallback

router: Router = Router()


@router.callback_query(AddTaskCallback.filter())
async def add_task_callback(call: types.CallbackQuery, callback_data: AddTaskCallback):
    await call.message.edit_text('Add Task!')


@router.callback_query(DeleteTaskCallback.filter())
async def delete_task_callback(call: types.CallbackQuery, callback_data: DeleteTaskCallback):
    await call.answer('Delete Task!')
