from .start import start_router
from .base import base_router
from .help import help_router
from .settings import settings_router
from .add_task import add_task_router
from .delete_task import delete_task_router
from .done_task import done_task_router
from .edit_task import edit_task_router

routers = [start_router,
           base_router,
           help_router,
           settings_router,
           add_task_router,
           delete_task_router,
           done_task_router,
           edit_task_router]

__all__ = [
    "start_router",
    "base_router",
    "help_router",
    "settings_router",
    "add_task_router",
    "delete_task_router",
    "done_task_router",
    "edit_task_router",
    "routers"
]
