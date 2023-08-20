""" File containing bot message templates """

from typing import List

from src.bot.states.data import SortingStateData, SortDirectionKey
from src.db.models.task import Task


def task_list(tasks: List[Task], title: str | None = None, empty_msg: str | None = None) -> str:
    message: str = ""
    if title:
        message += f"<b>{title}</b>\n-------------------------\n\n"
    if len(tasks) < 1:
        if empty_msg:
            message += f"<i>{empty_msg}</i>"
    else:
        for task in tasks:
            message += f"{done_marker(task.is_done)} "
            message += f"<b>{task.title}</b>\n"
            message += f"        <i>{task.description}</i>\n"
    return message


def get_text_sorting_button(date: SortingStateData, item: str, is_selected: bool = False):
    text: str = ""
    if is_selected:
        if date["is_ascending"]:
            text += "⏫"
        else:
            text += "⏬"
    else:
        text += "⏹"
    text += item

    return text


def get_markers_for_sorting_direction_key() -> dict:
    return {
        SortDirectionKey.CREATED_DATE: "📅",
        SortDirectionKey.TASKS: "📌",
        SortDirectionKey.DONE: "✅"
    }


def deletion_marker(is_delete: bool):
    return "❌" if is_delete else "🔘"


def enable_marker(is_enable: bool):
    return "🟢" if is_enable else "⭕️"


def done_marker(is_done: bool):
    return "✅" if is_done else "📌"


def bold_text(text: str):
    return f"<b>{text}</b>"


def italic_text(text: str):
    return f"<i>{text}</i>"
