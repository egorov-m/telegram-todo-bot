from enum import StrEnum


class LoggerType(StrEnum):
    BOT_LOGGER = "bot_logger"
    BOT_ERROR_LOGGER = "bot_error_logger"


class StatsType(StrEnum):
    CALLBACK_EVENT = "callback_event"
    STATE_EVENT = "state_event"


class BotEventType(StrEnum):
    MESSAGE = "message"
    CALLBACK_QUERY = "callback_query"


class ImageFormat(StrEnum):
    PNG = "png"
    JPG = "jpg"
    WEBP = "webp"
    SVG = "svg"
    PDF = "pdf"


class VisualizeFormat(StrEnum):
    PNG = "png"
    JPG = "jpg"
    WEBP = "webp"
    SVG = "svg"
    PDF = "pdf"
    HTML = "html"
    JSON = "json"
