from enum import IntEnum


class ToDoBotErrorCode(IntEnum):
    """
    Error codes of the telegram bot.

    Ranges:
           0-1000: general errors
        3001-4000: task errors
        4001-5000: user errors
        5001-6000: event errors
    """

    # 0-1000: general errors
    GENERIC_ERROR = 0

    # 3001-4000: task errors
    TASK_NOT_SPECIFIED = 3001
    TASK_NOT_FOUND = 3002

    # 4001-5000: user errors
    USER_NOT_SPECIFIED = 4001
    USER_DISABLED = 4002
    USER_NOT_FOUND = 4003
    USER_HAS_NOT_AGREEMENT_ACCEPTED = 4004

    # 5001-6000: event errors
    EVENT_NOT_FOUND = 5001


class ToDoBotError(Exception):
    """Base class for telegram bot exceptions."""

    message: str
    error_code: int

    def __init__(self,
                 message: str,
                 error_code: ToDoBotErrorCode,
                 *args):
        super().__init__(message, error_code, *args)
        self.message = message
        self.error_code = error_code

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(message='{self.message}', error_code={self.error_code})"
