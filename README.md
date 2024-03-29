<p align="center">
  <a href="https://github.com/egorov-m/telegram-todo-bot" target="blank"><img src="./assets/logo.jpg" width="150" alt="ToDo" /></a>
</p>
<h1 align="center">Telegram ToDo bot</h1>
<p align="center">Учебный проект, telegram бот для работы со списком задач.</p>

<p align="center">
    <a href="https://www.python.org/" target="blank">
        <img src="https://img.shields.io/badge/Python-000?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    </a>
    <a href="https://github.com/aiogram/aiogram" target="blank">
        <img src="https://img.shields.io/badge/Aiogram-000?style=for-the-badge&logo=aiogram&logoColor=white" alt="Aiogram">
    </a>
    <a href="https://www.postgresql.org/" target="blank">
        <img src="https://img.shields.io/badge/Postgres-000?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres">
    </a>
    <a href="https://www.sqlalchemy.org/" target="blank">
        <img src="https://img.shields.io/badge/SQLAlchemy-000?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
    </a>
    <a href="https://redis.io/" target="blank">
        <img src="https://img.shields.io/badge/Redis-000?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
    </a>
    <a href="https://plotly.com/python/" target="blank">
        <img src="https://img.shields.io/badge/Plotly-000?style=for-the-badge&logo=plotly&logoColor=white" alt="Redis">
    </a>
</p>

## Реализовано

### Базовые возможности

| № | Описание                       | Скриншоты (en)                                    | Скриншоты (ru)                                    |
| - |--------------------------------|---------------------------------------------------|---------------------------------------------------|
| 1 | Добавление новых задач         | ![imdge](./assets/screenshots/en/add_task.png)    | ![imdge](./assets/screenshots/ru/add_task.png)    |
| 2 | Удаление задач                 | ![imdge](./assets/screenshots/en/delete_task.png) | ![imdge](./assets/screenshots/ru/delete_task.png) |
| 3 | Отметка задач, как выполненных | ![imdge](./assets/screenshots/en/done_task.png)   | ![imdge](./assets/screenshots/ru/done_task.png)   |
| 4 | Редактирование задач           | ![imdge](./assets/screenshots/en/edit_task.png)   | ![imdge](./assets/screenshots/ru/edit_task.png)   |

### Особенности

| № | Описание                                      | Скриншоты (en) | Скриншоты (ru) |
| - |-----------------------------------------------|----------------|----------------|
| 1 | Локализация бота                              | —              | —              |
| 2 | Основное управление ботом через inline кнопки | —              | —              |

### Управление

Доступна панель администратора для управления пользователями и просмотра статистики.

| № | Описание                                                                                                                                                                                                                                                                                        | Скриншоты (en)                                                                                                      | Скриншоты (ru)                                                                                                      |
| - |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| 1 | **Пользователи:** просмотр списка пользователей бота по страницам (пагинация) — сортировка пользователей: по дате регистрации, по числу задач, числу выполненных; поиск пользователя по его данным (через отправку сообщений); возможность блокировать / разблокировать доступ для пользователя | ![imdge](./assets/screenshots/en/admin_panel_users.png)                                                             | ![imdge](./assets/screenshots/ru/admin_panel_users.png)                                                             |
| 2 | **Статистика:** вывод статистики по количеству событий  (callback / state) на таймлайне, возможность получить результат в различных форматах, оповещение о процессе формирования и визуализации статистики, регулирование временного интервала (для *.HTML интерактивно)                        | ![imdge](./assets/screenshots/en/admin_panel_stats_1.png) ![imdge](./assets/screenshots/en/admin_panel_stats_2.png) | ![imdge](./assets/screenshots/ru/admin_panel_stats_1.png) ![imdge](./assets/screenshots/ru/admin_panel_stats_2.png) |


### Ограничения

| № | Описание                                                                                                                                           | Скриншоты (en)                                 | Скриншоты (ru)                                 |
| - |----------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|------------------------------------------------|
| 1 | Доступ к admin панели и всем её функциям есть только у администратора                                                                              | —                                              | —                                              |
| 2 | Всем пользователям доступно место для хранения не более 20 задач одновременно                                                                      | ![imdge](./assets/screenshots/en/main.png)     | ![imdge](./assets/screenshots/ru/main.png)     |
| 3 | Пользователь, заблокированный администратор не имеет доступа к функционалу бота, на любое действие получает сообщение о блокировки                 | ![imdge](./assets/screenshots/en/lockout.png)  | ![imdge](./assets/screenshots/ru/lockout.png)  |
| 4 | Для доступа к функционалу бота пользователь должен принять пользовательское соглашение, в дальнейшем оно будет доступно для прочтения в настройках | ![image](./assets/screenshots/en/settings.png) | ![image](./assets/screenshots/ru/settings.png) |

## Реализация в перспективе

1. Локализация на большее число языков.
2. Сортировка, фильтрация, поиск по задачам.
3. Указание сроков для задач, напоминания об истечение срока, авто выполнение при истечение срока.
4. Admin panel: большая гибкость управления пользователями, назначения ролей; больше типов статистики с возможностью кастомизации напрямую через бота.
5. Реализация списка задач для групп, групповое управление задачами, назначение задач для пользователя и т.п.
6. Вынесение логике в отдельный сервис для реализации для других интерфейсов и интеграции со сторонними сервисами.
7. Внедрение моделей искусственного интеллекта для более гибкой аналитики бота, интуитивного упорядочивание задач, текстовых рекомендаций по улучшению рабочего процесса для пользователя на основе его ведения списка задач.
