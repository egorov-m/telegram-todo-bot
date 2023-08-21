# Commands for menu
cmd_start_title = /старт
cmd_start_description = Добро пожаловать! Начните использовать список быстрых дел.

cmd_help_title = /помощь
cmd_help_description = Справочное сообщение о возможностях telegram бота.

# Buttons
btn_start_title = Старт
btn_add_task_title = Добавить задачу ➕

btn_delete_task_title = Удалить задачу ❌
btn_delete_all_tasks_title = Удалить все 🟥
btn_delete_selected_tasks_title = Удалить выбранные ❌

btn_done_task_title = Выполнено ✅ | не выполнено 📌
btn_all_done_task_title = Выполнить все ❇️
btn_nothing_done_task = Ничего не выполнено 📌

btn_edit_task_title = Редактировать задачу ✏️
btn_edit_task_change_title = Изменить заголовок
btn_edit_task_change_description = Изменить описание

btn_update_list_title = Обновить список 🔄
btn_settings_title = Настройки ⚙️
btn_about_title = О боте ℹ️

btn_admin_panel = Панель администратора 🔑
btn_admin_panel_users = Пользователи 👤
btn_admin_panel_users_reset_search = Сбросить поиск 🔎 ({ $text })

btn_save_title = Сохранить ✅
btn_apply_title = Применить ☑️
btn_cancel_title = Отменить ◀️
btn_back_title = Назад ◀️
btn_skip_title = Пропустить ⤵️

btn_languages_title = Языки 🌐
btn_language_en_US_title = Английский 🇺🇸
btn_language_ru_RU_title = Русский 🇷🇺

# Messages
help_title = Вам нужно вести список дел?
help_message = Этот бот поможет вам в этом. Основное управление интуитивно, осуществляется кнопками. Для доступа к главному меню выполните команду /старт.

task_list_title = СПИСОК ЗАДАЧ 📝
task_list_empty_message = У вас ещё нет задач.

add_task_message = Добавление новой задачи 🆕
                   Заголовок: { $title }
                   Описание: { $description }
add_task_enter_title = Введите заголовок новой задачи:
add_task_enter_description = Введите описание новой задачи:
add_task_confirm = Сохранить новую задачу?

add_task_error_title = Добавление новой задачи 🆕
add_task_error_description = Был достигнут лимит { $limit } доступного хранилища задач. Добавление не доступно. Вы можете удалить старые задачи, а потом добавить новый, либо выполнить редактирование существующих.

delete_task_message_title = Удаление задач ❌
delete_task_message_subtitle = Нажимайте на кнопки для выбора
delete_task_info_message = Выбрано для удаления: { $count }

done_task_message_title = Отметка о выполнении заданий ✅
done_task_message_subtitle = Нажимайте кнопки для выполнения

edit_task_message_title = Редактирование ✏️
edit_task_message_subtitle = Нажмите на кнопку, чтобы выбрать задачу
edit_task_message_subtitle_task = Задача:
                                  { $is_done } { $title }
                                    { $description }
edit_task_message_subtitle_edit = Выберите, что нужно отредактировать
edit_task_message_enter_title = Введите новый заголовок задачи
edit_task_message_enter_description = Введите новое описание задачи

input_error_message = Введённые данные не корректны!

settings_title = Настройки бота ⚙️
settings_languages_title = Выберите язык для бота из доступных.

about_title = О боте ℹ️
about_description = Данный бот для работы со списками задач создан в образовательных целях.
                    Код проекта доступен в <a href="https://github.com/egorov-m/telegram-todo-bot">репозитории</a>.

error_message = Такое сообщение не может быть обработано, воспользуйтесь меню.
exception_message = В боте произошло исключение, которое не может быть обработано!

admin_panel_message_title = Администратор 🔑
admin_panel_message_admin_data = Id: { $id }
                                 Пользователь: @{ $username }
                                 Имя: { $first_name }
                                 Фамилия: { $last_name }
                                 Дата регистрации: { $created_date }
                                 Задач сейчас: { $task_now }
                                 Задач за всё время: { $task_all_time }
                                 Вы всего выполнили: { $you_done }
admin_panel_users_message_title = Пользователи 👤
admin_panel_users_message_subtitle = Нажимайте кнопки для настройки доступа пользователей.
                                     Отправляйте текстовые сообщения для выполнения поиска по данным пользователей.
admin_panel_users_message_user = доступ | пользователь | id | имя | фамилия | задач | выполнено

user_agreement_accepted_message = Пользовательское соглашение принято ✅
                                  Дата: { $date }

btn_user_agreement_title = Соглашение 🔏
btn_accept_user_agreement_title = Я принимаю пользовательское соглашение ☑️

user_lockout_message_title = Блокировка 🔒
user_lockout_message = Вы были заблокированы или не имеете доступа. Если вы считаете, что это ошибка, обратитесь к администратору.

user_agreement = Прежде чем начать использование данного бота, пожалуйста, ознакомьтесь с нашим пользовательским соглашением. Ваше использование бота означает ваше согласие с условиями, изложенными ниже:

                 1. Ответственность пользователя:
                 - Вы обязуетесь использовать бота только в законных целях и соблюдать все применимые законы и правила.
                 - Вы несете ответственность за любые данные, которые вы сохраняете или передаете через бота.
                 - Вы обязуетесь не использовать бота для распространения незаконного, оскорбительного, вредоносного или непристойного контента.

                 2. Конфиденциальность:
                 - Мы стремимся обеспечить конфиденциальность ваших данных. Однако, мы не можем гарантировать абсолютную безопасность передачи данных через интернет.
                 - Мы не будем передавать вашу личную информацию третьим лицам без вашего согласия, за исключением случаев, предусмотренных законом.

                 3. Отказ от ответственности:
                 - Мы не несем ответственности за любые убытки, прямые или косвенные, возникшие в результате использования бота.
                 - Мы не гарантируем непрерывную и безошибочную работу бота, и не несем ответственности за любые проблемы, возникшие в результате его использования.

                 4. Изменения в пользовательском соглашении:
                 - Мы оставляем за собой право вносить изменения в настоящее пользовательское соглашение. Изменения вступают в силу с момента их публикации.
