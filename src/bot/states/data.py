from enum import StrEnum
from typing import TypedDict


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
