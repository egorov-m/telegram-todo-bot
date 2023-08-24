""" File containing bot message templates """

from typing import List, Optional

from src.bot.structures.types import StatsType
from src.bot.states.data import SortingStateData, SortDirectionKey
from src.db.models.task import Task


def task_list(tasks: List[Task],
              *,
              current_count: int,
              count_limit: int = 20,
              title: Optional[str] = None,
              empty_msg: Optional[str] = None) -> str:
    message: str = ""
    if title:
        message += f"{bold_text(title)}\n-------------------------\n"
    if current_count < count_limit / 2:
        count_icon = "🪫"
    elif current_count == count_limit:
        count_icon = "💯"
    elif current_count > count_limit:
        count_icon = "☠️"
    else:
        count_icon = "🔋"
    message += bold_text(f"{count_icon} {current_count} / {count_limit}\n\n")
    if len(tasks) < 1:
        if empty_msg:
            message += italic_text(empty_msg)
    else:
        for task in tasks:
            message += f"{done_marker(task.is_done)} "
            message += f"{bold_text(task.title)}\n"
            message += f"        {italic_text(task.description)}\n"
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


def get_selected_stats_markers(selected_stats: list[StatsType]) -> list[dict[StatsType, str]]:
    markers: dict = {StatsType.STATE_EVENT: "✖️",
                     StatsType.CALLBACK_EVENT: "✖️"}
    for item in selected_stats:
        markers[item] = "✔️"

    return markers


def task_marker():
    return "🛠"


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
