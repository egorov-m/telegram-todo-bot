from enum import StrEnum
from typing import TypedDict


class AddTaskStateData(StrEnum):
    TASK_TITLE = "task_title"
    TASK_DESCRIPTION = "task_description"
    ADD_TASK_MESSAGE = "add_task_message"


class DeletableTask(TypedDict):
    task_id: str
    is_delete: bool
    is_done: bool
    title: str
