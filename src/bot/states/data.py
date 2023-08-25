from enum import StrEnum
from typing import TypedDict

from aiogram.types import Message

from src.bot.structures.types import StatsType, VisualizeFormat


class AddTaskStateData(TypedDict):
    task_title: str
    task_description: str
    add_task_message: Message


class DoneTask(TypedDict):
    task_id: str
    is_done: bool
    title: str


class DeletableTask(DoneTask):
    is_delete: bool


class EditTask(DoneTask):
    description: str


class EditTaskStateData(TypedDict):
    task: EditTask
    edit_task_message: Message


class SortDirectionKey(StrEnum):
    CREATED_DATE = "created_date"
    TASKS = "tasks"
    DONE = "done"


class SortingStateData(TypedDict):
    key: SortDirectionKey
    is_ascending: bool
    search_text: str
    message: str
    offset: int
    list_hash: str


class VisProcessData(TypedDict):
    selected_stats: list[StatsType]
    visualize_format: VisualizeFormat


class StatsStateData(TypedDict):
    in_process: list[VisProcessData]
    selected_stats: list[StatsType]
