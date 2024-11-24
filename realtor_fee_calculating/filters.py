from realtor_fee_calculating.dialog import FeeCalculating
from fsm import cache_storage
from bot_instance import bot
from telebot.types import CallbackQuery


def currency_callback_filter(call:CallbackQuery) -> str:
    valid_data = ('USD', 'EUR', 'CNY', 'BYN', 'RUB', 'cf_restart')
    return call.data in valid_data


def handle_keyboard_fee_calc(call:CallbackQuery) -> None:
    chat_id, user_id = call.message.chat.id, call.from_user.id
    match call.data:
        case "calc":
            FeeCalculating().send_greeting(chat_id, user_id)
        case 'USD'|'EUR'|'CNY'|'BYN'|'RUB':
            cache_storage.set_value(user_id, chat_id, 'cf_chosen_currency', call.data)
            FeeCalculating().price_for_fee_input(chat_id, user_id) 
        case 'cf_restart':
            FeeCalculating().restart(chat_id, user_id)   