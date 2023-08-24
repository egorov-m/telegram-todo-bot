""" File representing the translator for localization """

from re import split
import logging as log

from babel.core import Locale
from fluent.runtime import FluentLocalization, FluentResourceLoader


logger = log.getLogger('translator_logger')

default_locale: str = 'en_US'
locales: list[str] = [default_locale, 'ru_RU']
_loader: FluentResourceLoader = FluentResourceLoader('./src/lexicon/l10n/{locale}')
_localizations: dict[Locale, FluentLocalization] = {}
_localization_all: FluentLocalization = FluentLocalization(['all'], ['cmd.ftl'], _loader)


async def _add_localization(locale: str | Locale):
    locale = str(locale)
    if not locale in _localizations:
        _localizations[locale] = FluentLocalization([locale], ['main.ftl'], _loader)


async def load_localizations():
    for lc in locales:
        await _add_localization(lc)


class Translator:
    def __init__(self, locale: Locale = "en_US"):
        self.locale = locale
        self.localization: FluentLocalization = self.get_localization(locale)

    @staticmethod
    def get_localization(locale: str | Locale = "en_US") -> FluentLocalization:
        locale = str(locale)
        if len(_localizations) < 1:
            msg: str = 'The localization has not been loaded, use the load_localizations() method.'
            logger.error(msg)
            raise RuntimeError(msg)
        if not locale in locales:
            locale = default_locale
            logger.warning(f'The locale \'{locale}\' does\'t exist, the locale \'{default_locale}\' was used.')

        return _localizations[locale]

    async def translate(self, msg_id: str, **kwargs: dict[str, any]) -> str:
        return self.localization.format_value(msg_id, kwargs)


def translate_list_all(msg_id: str, **kwargs: dict[str, any]) -> list[str]:
    """
    A method to get all translations for all locales at once as a list
    example:
    translate_list_all('cmd_start')
    ['start', 'старт', ...] # Outputs a list of all translations for the start command
    """
    return split("\n+", _localization_all.format_value(msg_id, kwargs))
