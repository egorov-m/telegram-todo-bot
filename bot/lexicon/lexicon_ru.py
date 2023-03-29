from dataclasses import dataclass
from lexicon.lexicon import LEXICON, buttons


@dataclass()
class LEXICON_RU(LEXICON):
    start_command: str = "Добро пожаловать! Вас приветствует бот для ведения быстрого списка дел."
    help_command: str = "Справочное сообщение."
    buttons = buttons(config='Настройки ⚙️',
                      add_task='Добавить задачу ➕',
                      task_list='Список задач 🗒')
