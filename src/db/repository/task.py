from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db.models import Task, Telegram_User, User


class TaskRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_task(self, title: str, description: str, telegram_user: Telegram_User):
        task: Task = Task(title=title,
                          description=description,
                          reg_telegram_user_id=telegram_user.telegram_user_id,
                          id_user=telegram_user.id_user)
        self.session.add(task)
        await self.session.commit()

    async def get_task(self, task_id: UUID) -> Task:
        return await self.session.execute(select(Task).where(Task.id == task_id))

    async def get_tasks_for_user(self, user: User) -> list[Task]:
        return await self.session.execute(select(Task).where(Task.id_user == user.id))

    async def get_tasks_for_telegram_user(self, user: Telegram_User) -> list[Task]:
        return await self.session.execute(select(Task).where(Task.reg_telegram_user_id == user.telegram_user_id))

    async def get_all_tasks(self) -> list[Task]:
        return await self.session.execute(select(Task))

    async def update_task(self, task_id: UUID, **kwargs: [str, any]):
        task: Task = self.get_task(task_id)
        task.title = kwargs["title"]
        task.description = kwargs["description"]
        task.is_done = kwargs["is_done"]
        task.is_exist = kwargs["is_exist"]
        await self.session.commit()
