from abc import ABC
import telebot
from decimal import Decimal
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telebot.states.sync.context import StateContext
from bot_instance import bot
from fsm import cache_storage, UserStates
from realtor_fee_calculating.fee_calc_functions import get_currency_rates, calculate_fee
from utils import update_msg_to_del, del_msg


class FeeCalculatingTypes(ABC):
    def __init__(self):
        super().__init__()


    def create_keyboard1(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('💵 ДОЛЛАР США', callback_data='USD'))
        keyboard.add(InlineKeyboardButton('💶 ЕВРО', callback_data='EUR'))
        keyboard.add(InlineKeyboardButton('🇨🇳 КИТАЙСКИЙ ЮАНЬ', callback_data='CNY'))
        keyboard.add(InlineKeyboardButton('🇧🇾 БЕЛОРУССКИЙ РУБЛЬ', callback_data='BYN'))
        keyboard.add(InlineKeyboardButton('🇷🇺 РОССИЙСКИЙ РУБЛЬ', callback_data='RUB'))
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.add(InlineKeyboardButton('⚒ В главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard2():
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('В главное меню', callback_data='menu'), InlineKeyboardButton('Рестарт', callback_data='cf_restart'))
        return keyboard


    def create_keyboard3(self):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('В главное меню', callback_data='menu'), InlineKeyboardButton('Рестарт', callback_data='cf_restart'))
        return keyboard


class FeeCalculating(FeeCalculatingTypes):
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self) -> None:
        super().__init__()


    def send_greeting(self, chat_id, user_id) -> None:
        del_msg(chat_id, user_id)
        with open('./content/calc_fee/hello.jpg', "rb") as img1:
            bot.send_photo(chat_id, img1, caption="Эта функция поможет вам рассчитать стоимость риэлторских услуг. Я могу учитывать разные валюты. Для начала выберите валюту, в которой вы хотите получить результат.")
        to_del = bot.send_message(chat_id, "Меню:", reply_markup=self.create_keyboard1())
        update_msg_to_del(chat_id, user_id, to_del)


    def price_for_fee_input(self, chat_id, user_id, state:StateContext) -> None:
        state.set(UserStates.waiting_price_for_fee)
        cf_chosen_currency = cache_storage.get_value(f'cf_chosen_currency:{chat_id}')
        mes_del = cache_storage.get_value(f'cf_cur_sel_del:{chat_id}')
        del_msg(chat_id, user_id)
        with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/calc_fee/price.jpg', 'rb') as img1:
            bot.send_photo(chat_id, img1, caption=f"Пожалуйста, введите стоимость квартиры в {cf_chosen_currency}.")
        to_del = bot.send_message(chat_id, "Меню", reply_markup=self.create_keyboard2())
        update_msg_to_del(chat_id, user_id, to_del)


    @bot.message_handler(state=UserStates.waiting_price_for_fee)
    def validate_price_input(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        cf_chosen_currency = cache_storage.get_value(user_id, chat_id, 'cf_chosen_currency')
        cf_price_input = message.text
        try:
            cf_price = int(cf_price_input)
        except ValueError:
            bot.send_message(user_id, "Сумма должна быть целым числом, пожалуйста повторите ввод.", reply_to_message_id=message.message_id)
            return self.validate_price_input(chat_id)
        if cf_price < 1 or cf_price > 100000000000:
            bot.send_message(user_id, "Сумма не может быть отрицательной, пожалуйста повторите ввод.", reply_to_message_id=message.message_id)
            return  self.validate_price_input(chat_id)
        if cf_price_input != str(cf_price):
            bot.send_message(user_id, "Неправильный формат ввода, пожалуйста повторите ввод.", reply_to_message_id=message.message_id)
            return self.validate_price_input(chat_id)
        cf_price = Decimal(cf_price)
        cache_storage.set_value(f'cf_price:{chat_id}', cf_price)
        cf_currency = get_currency_rates(chat_id)
        cf_percent, cf_fee = calculate_fee(chat_id)
        with open('./content/rent/forecast.jpg', 'rb') as img1:
            bot.send_photo(chat_id, img1, caption=f"Стоимость риэлторской услуги в вашем случае составит {int(cf_percent)} {cf_chosen_currency}, {cf_fee * 100}%.")
        to_del = bot.send_photo(chat_id, "Меню", reply_markup=self.create_keyboard3())
        update_msg_to_del(chat_id, user_id, to_del)


    def restart(self, chat_id, user_id):
        del_msg(chat_id, user_id)
        self.send_greeting(chat_id, user_id)



    