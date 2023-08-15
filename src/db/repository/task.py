from typing import Optional
from uuid import UUID

from sqlalchemy import update, and_
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.db.models import Task, User
from src.db.utils import menage_db_method, CommitMode
from src.exceptions import ToDoBotError, ToDoBotErrorCode


class TaskRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    @menage_db_method(CommitMode.FLUSH)
    async def create_task(self,
                          title: str,
                          description: str,
                          creator_telegram_user_id: int,
                          is_done: bool = False,
                          is_exist: bool = True) -> Task:
        if len(title) > 64:
            raise ToDoBotError("The task title can't be longer than 64 characters", ToDoBotErrorCode.TASK_NOT_SPECIFIED)
        if len(description) > 256:
            raise ToDoBotError("The task description can't be longer than 256 characters", ToDoBotErrorCode.TASK_NOT_SPECIFIED)

        new_task: Task = Task(title=title,
                              description=description,
                              creator_telegram_user_id=creator_telegram_user_id,
                              is_done=is_done,
                              is_exist=is_exist)

        self.session.add(new_task)
        return new_task

    async def get_task(self, task_id: UUID, is_existed: bool = True) -> Task:
        task = await self.session.get(Task, task_id)
        if is_existed:
            if not task.is_exist:
                task = None

        if task is None:
            raise ToDoBotError("Task not found", ToDoBotErrorCode.TASK_NOT_FOUND)

        return task

    async def get_tasks_for_user(self, user: User, is_existed: bool = True) -> list[Task]:
        if is_existed:
            result: Result = await self.session.execute(
                select(Task)
                .where(and_(Task.creator_telegram_user_id == user.telegram_user_id, Task.is_exist == True))
                .order_by(Task.title)
            )
        else:
            result: Result = await self.session.execute(
                select(Task)
                .where(Task.creator_telegram_user_id == user.telegram_user_id)
                .order_by(Task.title)
            )

        return result.scalars().all()

    @menage_db_method(CommitMode.FLUSH)
    async def update_task(self,
                          task_id: UUID,
                          *,
                          title: Optional[str] = None,
                          description: Optional[str] = None,
                          is_done: Optional[bool] = None,
                          is_exist: Optional[bool] = None) -> Task:
        task: Task = await self.get_task(task_id)

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if is_done is not None:
            task.is_done = is_done
        if is_exist is not None:
            task.is_exist = is_exist

        return task

    @menage_db_method(CommitMode.FLUSH)
    async def update_status_task(self, task_id: UUID, is_done: bool) -> Task:
        task: Task = await self.get_task(task_id)
        task.is_done = is_done
        return task

    @menage_db_method(CommitMode.FLUSH)
    async def done_task(self, task_id: UUID, is_done: bool = True, active_telegram_user_id: int | None = None) -> Task:
        task: Task = await self.get_task(task_id)
        if active_telegram_user_id is not None:
            if task.creator_telegram_user_id != active_telegram_user_id:
                raise ToDoBotError(message="A user cannot done another user's task",
                                   error_code=ToDoBotErrorCode.USER_NOT_SPECIFIED)
        task.is_done = is_done
        return task

    @menage_db_method(CommitMode.FLUSH)
    async def done_tasks_for_user(self, user: User, is_done: bool = True):
        await self.session.execute(
            update(Task).where(Task.creator_telegram_user_id == user.telegram_user_id).values(is_done=is_done)
        )

    @menage_db_method(CommitMode.FLUSH)
    async def delete_task(self, task_id: UUID, active_telegram_user_id: int | None = None) -> Task:
        task: Task = await self.get_task(task_id)
        if active_telegram_user_id is not None:
            if task.creator_telegram_user_id != active_telegram_user_id:
                raise ToDoBotError(message="A user cannot delete another user's task",
                                   error_code=ToDoBotErrorCode.USER_NOT_SPECIFIED)
        task.is_exist = False
        return task

    @menage_db_method(CommitMode.FLUSH)
    async def delete_tasks_for_user(self, user: User):
        await self.session.execute(
            update(Task).where(Task.creator_telegram_user_id == user.telegram_user_id).values(is_exist=False)
        )
