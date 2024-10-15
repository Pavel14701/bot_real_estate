from telebot import custom_filters
from bot_instance import bot

from filters import handle_keyboard

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())
from telebot.states.sync.middleware import StateMiddleware
bot.setup_middleware(StateMiddleware(bot))

if __name__ == '__main__':
    bot.infinity_polling()