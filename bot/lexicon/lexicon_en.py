from dataclasses import dataclass
from lexicon.lexicon import LEXICON, buttons


@dataclass()
class LEXICON_EN(LEXICON):
    start_command: str = "Welcome! This is a bot for keeping a fast todo list."
    help_command: str = "Help message."
    buttons = buttons(config='Settings ⚙️',
                      add_task='Add Task ➕',
                      task_list='Task list 🗒')
