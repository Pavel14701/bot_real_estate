from abc import ABC
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class MainTypes(ABC):
    def __init__(self):
        ABC.__init__(self)

    def create_keyboard() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🤖 Кузя - ваш помошник на базе AI", callback_data="kuzia_chatbotai"))
        keyboard.add(InlineKeyboardButton("🔍 Анализ рыночной цены", callback_data="price"))
        keyboard.add(InlineKeyboardButton("🧮 Калькулятор риэлторских услуг", callback_data="calc"))
        keyboard.add(InlineKeyboardButton("💵 Анализ прибыльности сдачи квартиры в аренду", callback_data="rent"))
        #keyboard.add(InlineKeyboardButton("🧠 Аналитика", callback_data="analytics"))
        #keyboard.add(InlineKeyboardButton("Подбор квартиры по характеристикам", callback_data="search"))
        keyboard.add(InlineKeyboardButton("😎 Услуги", callback_data="services"))
        return keyboard