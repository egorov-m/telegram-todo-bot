from dataclasses import dataclass
from typing import List

from lexicon.lexicon import LEXICON, button
from models.task import Task


@dataclass()
class LEXICON_EN(LEXICON):
    commands = {'/start': 'Welcome! Start using the fast to-do list.',
                '/help': 'A help message about the bot\'s capabilities.'}
    main_buttons = {'Add Task ➕': 'btn_add_task',
                    'Delete Task ❌': 'btn_delete_task',
                    'Done ✅ | not done 📌': 'btn_done_not_done',
                    'Edit Task ✏️': 'btn_edit_task',
                    'Update list 🔄': 'btn_update_list',
                    'Settings ⚙️': 'btn_settings'}
    delete_all_button = button('Delete All ❌', 'btn_delete_all_tasks')
    save_delete_tasks_button = button(
        'Save ✅', 'btn_save_delete_tasks')
    cancel_button = button('Cancel ◀️', 'btn_cancel')
    save_edit_task_button = button('Save ✅', 'btn_save_edit_task')
    error_message: str = 'Such a message can\'t be processed, use the menu.'

    @staticmethod
    def start_command(tasks: List[Task]) -> str:
        message: str = '<b>TODO LIST</b> 📝\n----------------------\n\n'
        if len(tasks) < 1:
            message.Add('You don\'t have tasks yet.')
        else:
            for task in tasks:
                if task.isDone:
                    message += '✅ '
                else:
                    message += '⏺ '
                message += f'<b>{task.title}</b>\n'
                message += f'        <i>{task.description}</i>\n'
        return message
