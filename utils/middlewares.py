from telebot import TeleBot
from telebot.types import CallbackQuery
from utils.utils import log_exceptions, logger


class LogExceptionMiddlewareMeta(type):
    def __new__(cls, name, bases, dct:dict):
        for attr, value in dct.items():
            if callable(value) and not attr.startswith("__"):
                dct[attr] = log_exceptions(value)
        return super().__new__(cls, name, bases, dct)


class AnswerCallbackMiddleware(meta_class=LogExceptionMiddlewareMeta):
    def __init__(self, bot:TeleBot):
        self.bot = bot


    def __call__(self, call: CallbackQuery):
        try:
            self.bot.answer_callback_query(call.id, "Done", show_alert=False)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)