from telebot import custom_filters
from utils.middlewares import AnswerCallbackMiddleware
from commands import menu
from realtor_fee_calculating.filters import handle_keyboard_fee_calc, currency_callback_filter
from rental_profitable.filters import handle_keyboard_rental, rental_callback_filter
from bids_requests.filters import BidsCallbackFilter
from cost_comp_analysis.filters import CostCompCallbackFilter
from bot_instance import bot, BotWebhooks
from configs import Configs
from daemon.main import *

bot.message_handler(commands=['start'])(menu)
bot.callback_query_handler(func=currency_callback_filter)(handle_keyboard_fee_calc)
bot.callback_query_handler(func=rental_callback_filter)(handle_keyboard_rental)
bot.callback_query_handler(func=CostCompCallbackFilter().region_choice_callback_filter)(CostCompCallbackFilter().handle_keyboard_region_choice)
bot.callback_query_handler(func=CostCompCallbackFilter().cost_comp_callback_filter)(CostCompCallbackFilter().handle_keyboard_house_type)
bot.callback_query_handler(func=CostCompCallbackFilter().house_mat_callback_filter)(CostCompCallbackFilter().handle_keyboard_house_mat)
bot.callback_query_handler(func=CostCompCallbackFilter().house_type_callback_filter)(CostCompCallbackFilter().handle_keyboard_house_type)
bot.callback_query_handler(func=CostCompCallbackFilter().number_rooms_callback_filter)(CostCompCallbackFilter().handle_keyboard_number_rooms)
bot.callback_query_handler(func=CostCompCallbackFilter().price_finishing_callback_filter)(CostCompCallbackFilter().handle_keyboard_price_finishing)
bot.callback_query_handler(func=CostCompCallbackFilter().cac_back_callback_filter)(CostCompCallbackFilter().handle_keyboard_price_finishing)
bot.callback_query_handler(func=BidsCallbackFilter().bids_requests_callback_filter)(BidsCallbackFilter().handle_keyboard_bids_requests)


bot.add_callback_query_handler(AnswerCallbackMiddleware(bot))
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())
from telebot.states.sync.middleware import StateMiddleware
bot.setup_middleware(StateMiddleware(bot))


if __name__ == '__main__':
    if Configs.USE_WEBHOOK:
        BotWebhooks().run()
    else:
        bot.infinity_polling()