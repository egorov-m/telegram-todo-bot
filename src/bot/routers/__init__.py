from .start import start_router
from .base import base_router
from .help import help_router
from .settings import settings_router
from .add_task import add_task_router

routers = [start_router,
           base_router,
           help_router,
           settings_router,
           add_task_router]

__all__ = [routers]
