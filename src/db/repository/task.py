""" Task repository file """

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID, DATE, TIMESTAMP, BIGINT

from ..models import Task
from .abstract import Repository


class TaskRepo(Repository[Task]):
    """
    Task repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize task repository
        """
        super().__init__(type_model=Task, session=session)

    async def new(self,
                  title: Optional[str],
                  reg_telegram_user_id: Optional[BIGINT],
                  reg_date: Optional[DATE],
                  reg_time: Optional[TIMESTAMP],
                  id_user: Optional[UUID],
                  isDone: Optional[bool] = False,
                  isExist: Optional[bool] = True,
                  description: Optional[str] = None
                  ) -> Task:
        """
        Insert a new task for user into the database
        :param title Title for a new task
        :param reg_telegram_user_id The id of the telegram user registering the task
        :param reg_date Date of task registration
        :param reg_time Time of task registration
        :param id_user The id of the user registering the task
        :param isDone Is the task marked as down
        :param isExist Whether there is a task for the user (has not been deleted)
        :param description Description of the tasks
        """

        new_task = await self.session.merge(
            Task(
                title=title,
                reg_telegram_user_id=reg_telegram_user_id,
                reg_date=reg_date,
                reg_time=reg_time,
                id_user=id_user,
                isDone=isDone,
                isExist=isExist,
                description=description
            )
        )

        return new_task
