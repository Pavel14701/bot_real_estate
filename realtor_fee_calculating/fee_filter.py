from realtor_fee_calculating.fee_calc import FeeCalculating
from fsm import cache_storage
from bot_instance import bot
from telebot.types import CallbackQuery

@bot.callback_query_handler(func=lambda call: call.data in ['USD', 'EUR', 'CNY', 'BYN', 'RUB', 'cf_restart'])
def handle_keyboard_fee_calc(call:CallbackQuery):
    data = call.data
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    match call.data:
        case "calc":
            FeeCalculating().send_greeting(chat_id, user_id)
        case 'USD'|'EUR'|'CNY'|'BYN'|'RUB':
            cache_storage.set_value(user_id, chat_id, 'cf_chosen_currency', call.data)
            FeeCalculating().price_for_fee_input(chat_id, user_id) 
        case 'cf_restart':
            FeeCalculating().restart(chat_id, user_id)   