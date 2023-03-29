from dataclasses import dataclass


@dataclass()
class LEXICON:
    start_command: str
    help_command: str
    buttons: buttons
    languages: languages = languages()


@dataclass()
class languages:
    en: str = 'English 🇬🇧'
    ru: str = 'Russian 🇷🇺'


@dataclass()
class buttons:
    config: str
    add_task: str
    task_list: str
