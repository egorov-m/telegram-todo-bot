from dataclasses import dataclass, field
from typing import List

from models.task import Task


@dataclass()
class languages:
    en: str = 'English 🇬🇧'
    ru: str = 'Russian 🇷'


@dataclass()
class button:
    text: str
    data: str


@dataclass()
class LEXICON:
    commands = {}
    main_buttons = {}
    delete_all_button = None
    save_delete_tasks_button = None
    save_edit_task_button = None
    cancel_button = None
    languages = None
    error_message: str = 'Error!'

    @staticmethod
    def start_command(tasks: List[Task]) -> str:
        pass
