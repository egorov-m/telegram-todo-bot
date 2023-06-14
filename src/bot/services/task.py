from typing import List
from datetime import date, datetime

from src.db.models.user import User
from src.db.models.task import Task


class TaskService:
    async def get_tasks_for_user(self, user: User) -> List[Task]:
        list_task: List[Task] = [Task(title='Test task 1',
                                      description='description',
                                      reg_telegram_user_id=12345,
                                      reg_date=date.today(),
                                      reg_time=datetime.now().timestamp(),
                                      isDone=False,
                                      isExist=True,
                                      id_user='12345'),
                                 Task(title='Test task 2',
                                      description='description',
                                      reg_telegram_user_id=12345,
                                      reg_date=date.today(),
                                      reg_time=datetime.now().timestamp(),
                                      isDone=True,
                                      isExist=True,
                                      id_user='12345')]
        return list_task
