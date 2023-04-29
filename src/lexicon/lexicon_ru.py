from dataclasses import dataclass

from lexicon.lexicon import LEXICON, button


@dataclass()
class LEXICON_RU(LEXICON):
    commands = {'/start': 'Добро пожаловать! Начните использовать список быстрых дел.',
                '/help': 'Справочное сообщение о возможностях telegram бота.'}
