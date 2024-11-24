from telebot.types import CallbackQuery
from bids_requests.dialog import BidRequests
from fsm import cache_storage


class BidsCallbackFilter:
    def bids_requests_callback_filter(self, call:CallbackQuery) -> str:
        return call.data in ('services_sell', 'services_buy', 'services_docs', 'services_sell_final')

    def handle_keyboard_bids_requests(self, call:CallbackQuery) -> None:
        chat_id, user_id = call.message.chat.id, call.from_user.id
        match call.data:
            case 'services_sell':
                cache_storage.set_value(user_id, chat_id, 'type_of_service', 'sell')
                return BidRequests().services_sell(chat_id, user_id)
            case 'services_buy':
                cache_storage.set_value(user_id, chat_id, 'type_of_service', 'buy')
                return BidRequests().services_sell(chat_id, user_id)
            case 'services_docs':
                cache_storage.set_value(user_id, chat_id, 'type_of_service', 'docs')
                return BidRequests().services_sell(chat_id, user_id)
            case 'services_sell_final':
                return BidRequests().services_bid_send(chat_id=chat_id, user_id=user_id)