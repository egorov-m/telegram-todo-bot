from enum import IntEnum
from functools import wraps

from src.exceptions import ToDoBotError, ToDoBotErrorCode
from src.db.models import User
from src.bot.structures.role import Role


class CommitMode(IntEnum):
    """
    Commit modes for the managed db methods
    """

    NONE = 0
    FLUSH = 1
    COMMIT = 2
    ROLLBACK = 3


def menage_db_method(auto_commit: CommitMode = CommitMode.FLUSH):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            result = await f(self, *args, **kwargs)
            match auto_commit:
                case CommitMode.FLUSH:
                    await self.session.flush()
                case CommitMode.COMMIT:
                    await self.session.commit()
                case CommitMode.ROLLBACK:
                    await self.session.rollback()

            return result

        return wrapped_f

    return decorator


def manage_data_protection_method(*available_user_roles: list[Role]):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, active_user: User, *args, **kwargs):
            if not active_user.role in available_user_roles:
                raise ToDoBotError(f"Only the {[item.name for item in available_user_roles]} can perform this operation.",
                                   ToDoBotErrorCode.USER_NOT_SPECIFIED)

            result = await f(self, active_user, *args, **kwargs)

            return result

        return wrapped_f

    return decorator
