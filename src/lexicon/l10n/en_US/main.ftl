# Commands for menu
cmd_start_title = /start
cmd_start_description = Welcome! Start using the fast to-do list.

cmd_help_title = /help
cmd_help_description = A help message about the bot's capabilities.

# Buttons
btn_start_title = Start
btn_add_task_title = Add Task ➕

btn_delete_task_title = Delete Task ❌
btn_delete_all_tasks_title = Delete all 🟥
btn_delete_selected_tasks_title = Delete selected ❌

btn_done_task_title = Done ✅ | not done 📌
btn_all_done_task_title = Done all ❇️
btn_nothing_done_task = Done nothing 📌

btn_edit_task_title = Edit Task ✏️
btn_edit_task_change_title = Change title
btn_edit_task_change_description = Change description

btn_update_list_title = Update list 🔄
btn_settings_title = Settings ⚙️
btn_about_title = About ℹ️

btn_admin_panel = Admin panel 🔑
btn_admin_panel_users = Users 👤

btn_save_title = Save ✅
btn_apply_title = Apply ☑️
btn_cancel_title = Cancel ◀️
btn_back_title = Back ◀️
btn_skip_title = Skip ⤵️

btn_languages_title = Languages 🌐
btn_language_en_US_title = English 🇺🇸
btn_language_ru_RU_title = Russian 🇷🇺

# Messages
help_title = Do you need to keep a to-do list?
help_message = This bot will help you with that. The main control is intuitive, done with buttons. To access the main menu, run the /start command.

task_list_title = TODO LIST 📝
task_list_empty_message = You don't have tasks yet.

add_task_message = Adding a new task 🆕
                   Title: { $title }
                   Description: { $description }
add_task_enter_title = Enter the title of the new task:
add_task_enter_description = Enter the description of the new task:
add_task_confirm = Save a new task?

add_task_error_title = Adding a new task 🆕
add_task_error_description = The { $limit } limit of available task storage has been reached. Addition is not available. You can delete old tasks and then add a new one, or you can edit existing tasks.

delete_task_message_title = Deleting tasks ❌
delete_task_message_subtitle = Press the buttons to select
delete_task_info_message = Selected for deletion: { $count }

done_task_message_title = Marking the done of tasks ✅
done_task_message_subtitle = Press the buttons to done

edit_task_message_title = Editing ✏️
edit_task_message_subtitle = Press the button to select a task
edit_task_message_subtitle_task = Task:
                                  { $is_done } { $title }
                                    { $description }
edit_task_message_subtitle_edit = Select what you want to edit
edit_task_message_enter_title = Enter a new task title
edit_task_message_enter_description = Enter a new task description

input_error_message = The data entered is not correct!

settings_title = Bot settings ⚙️
settings_languages_title = Select the language for the bot from the available.

about_title = About ℹ️
about_description = This task list bot is created for educational purposes.
                    The project code is available in the <a href="https://github.com/egorov-m/telegram-todo-bot">repository</a>.

error_message = Such a message can't be processed, use the menu.
exception_message = An exception occurred in the bot that couldn't be handled!

admin_panel_message_title = Administrator 🔑
admin_panel_message_admin_data = Id: { $id }
                                 Username: @{ $username }
                                 First name: { $first_name }
                                 Last name: { $last_name }
                                 Date of registration: { $created_date }
                                 Task now: { $task_now }
                                 Tasks all time: { $task_all_time }
                                 You've all done: { $you_done }
admin_panel_users_message_title = Users 👤
admin_panel_users_message_subtitle = Press the buttons to adjust user access
admin_panel_users_message_user = access | username | id | first_name | last_name | tasks | done

user_agreement_accepted_message = User agreement accepted ✅
                                  Date: { $date }

btn_user_agreement_title = User agreement 🔏
btn_accept_user_agreement_title = I accept the user agreement ☑️

user_lockout_message_title = Lockout 🔒
user_lockout_message = You have been blocked or do not have access. If you think this is an error, please contact an administrator.

user_agreement = Before using this bot, please read and agree to our terms of service. By using the bot, you agree to the following terms:

                 1. User Responsibility:
                 - You agree to use the bot only for lawful purposes and comply with all applicable laws and regulations.
                 - You are responsible for any data you store or transmit through the bot.
                 - You agree not to use the bot to distribute illegal, offensive, harmful, or indecent content.

                 2. Privacy:
                 - We strive to ensure the privacy of your data. However, we cannot guarantee absolute security of data transmission over the internet.
                 - We will not disclose your personal information to third parties without your consent, except as required by law.

                 3. Disclaimer:
                 - We are not liable for any direct or indirect losses incurred as a result of using the bot.
                 - We do not guarantee uninterrupted and error-free operation of the bot and are not responsible for any issues arising from its use.

                 4. Changes to the Terms of Service:
                 - We reserve the right to modify these terms of service. Changes will be effective upon posting.
