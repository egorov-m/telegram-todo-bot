""" File representing the translator for localization """

import logging as log
from typing import List, Dict, Any, Union

from babel.core import Locale
from fluent.runtime import FluentLocalization, FluentResourceLoader


logger = log.getLogger('translator_logger')

default_locale: str = 'en_US'
locales: List[str] = [default_locale, 'ru_RU']
_loader: FluentResourceLoader = FluentResourceLoader('./src/lexicon/l10n/{locale}')
_localizations: Dict[Locale, FluentLocalization] = {}


async def _add_localization(locale: str | Locale):
    locale = str(locale)
    if not locale in _localizations:
        _localizations[locale] = FluentLocalization([locale], ['main.ftl'], _loader)


async def load_localizations():
    async for lc in locales:
        await _add_localization(lc)


class Translator:
    def __init__(self, locale: Locale = "en_US"):
        self.locale = locale
        self.localization: FluentLocalization = await self.get_localization(locale)

    @staticmethod
    async def get_localization(locale: str | Locale = "en_US") -> FluentLocalization:
        locale = str(locale)
        if len(_localizations) < 1:
            await load_localizations()
        if not locale in locales:
            locale = default_locale
            logger.warning(f'The locale \'{locale}\' does\'t exist, the locale \'{default_locale}\' was used.')

        return _localizations[locale]

    async def translate(self, msg_id: str, args: Union[Dict[str, Any], None] = None) -> str:
        return await self.localization.format_value(msg_id, args)
