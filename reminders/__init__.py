from fsm import cache_storage
from bot_instance import bot

def send_reminders():
    reminder_states = cache_storage.get_all_reminder_states()
    for chat_id, state in reminder_states.items():
        try:
            if state == 'cac_started':
                message = 'Похоже, вы забыли обо мне😥! Чем я могу помочь сегодня?'
            elif state == 'cac_in_progress':
                message = 'Я заметил, что вы не завершили ваш запрос. Есть что-то, в чем я могу помочь?'
            elif state == 'r_in_started':
                message = 'Похоже, вы забыли обо мне😥! Чем я могу помочь сегодня?'
            elif state == 'r_in_progress':
                message = 'Я заметил, что вы не завершили ваш запрос. Есть что-то, в чем я могу помочь?'
            bot.send_message(chat_id, message)
        except Exception as e:
            pass