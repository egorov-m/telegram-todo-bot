from enum import StrEnum
from typing import TypedDict

from aiogram.types import Message


class AddTaskStateData(StrEnum):
    TASK_TITLE = "task_title"
    TASK_DESCRIPTION = "task_description"
    ADD_TASK_MESSAGE = "add_task_message"


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
