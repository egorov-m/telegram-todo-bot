""" File containing bot message templates """

from typing import List

from src.db.models.task import Task


def task_list(tasks: List[Task], title: str | None = None, empty_msg: str | None = None) -> str:
    message: str = ''
    if title:
        message += f'<b>{title}</b>\n-------------------------\n\n'
    if len(tasks) < 1:
        if empty_msg:
            message += f'<i>{empty_msg}</i>'
    else:
        for task in tasks:
            if task.is_done:
                message += '✅ '
            else:
                message += '⏺ '
            message += f'<b>{task.title}</b>\n'
            message += f'        <i>{task.description}</i>\n'
    return message


def bold_text(text: str):
    return f'<b>{text}</b>'


def italic_text(text: str):
    return f'<i>{text}</i>'
