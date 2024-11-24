from fsm import cache_storage
from telebot.types import CallbackQuery
from rental_profitable.dialog import RentProfitable



def rental_callback_filter(call:CallbackQuery) -> str:
    valid_data = (
        'rent', 'r_property_appreciation', 'r_restart', 'r_share',
        'r_1room', 'r_2room', 'r_3room', 'r_4room', 'r_5room',
        'back_to_rnor', 'back_to_rmc', 'back_to_rrp', 'back_to_rfp',
        'back_to_raa', 'back_to_rpa')
    return call.data in valid_data

def handle_keyboard_rental(call:CallbackQuery) -> None:
    chat_id, user_id, message = call.message.chat.id, call.from_user.id, call.message
    match call.data:
        case 'rent':
            RentProfitable().send_greeting(chat_id, user_id)
        case 'r_property_appreciation':
            RentProfitable().property_appreciation(message)
        case 'r_restart':
            RentProfitable().restart(message)
        case 'r_share'|'r_1room'|'r_2room'|'r_3room'|'r_4room'|'r_5room':
            cache_storage.set_value(user_id, chat_id, 'r_num_of_rooms', call.data)
            RentProfitable().forecast_period(chat_id, user_id) 
        case 'back_to_rpa':
            RentProfitable().property_appreciation(message)
        case 'back_to_raa':
            RentProfitable().apartment_area(chat_id, user_id)
        case 'back_to_rfp':
            RentProfitable().forecast_period(chat_id, user_id)
        case 'back_to_rrp':
            RentProfitable().rental_price(chat_id, user_id)
        case 'back_to_rmc':
            RentProfitable().maintenance_cost(chat_id, user_id)
        case 'back_to_rnor':
            RentProfitable().number_of_rooms(chat_id, user_id)