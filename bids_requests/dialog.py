from contextlib import suppress
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,\
    KeyboardButton, ReplyKeyboardRemove, Message
from telebot.states.sync.context import StateContext
from bot_instance import bot
from fsm import UserStates, cache_storage
from utils.utils import del_msg, update_msg_to_del, send_image, create_msg_thread, logger 
from utils.data import UserBid
from bids_requests.functions import EmailTgSendler


#TO DO Adding aplications into database
class BidRequestsMarkup:
    def create_keyboard1(self) -> InlineKeyboardMarkup:
        # sourcery skip: class-extract-method
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Продажа недвижимости под ключ', callback_data='services_sell'))
        keyboard.add(InlineKeyboardButton('Поиск дома мечты', callback_data='services_buy'))
        keyboard.add(InlineKeyboardButton('Помощь в оформлении документов и регистрации', callback_data='services_docs'))
        keyboard.add(InlineKeyboardButton('Главное меню', callback_data='menu'))
        return keyboard

    def create_keyboard2(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.add(KeyboardButton('Оставить заявку', request_contact=True))
        return keyboard

    def create_keyboard3(self, chat_id:int|str, user_id:int|str) -> InlineKeyboardMarkup:
        type_of_service = cache_storage.get_value(user_id, chat_id, 'type_of_service')
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Написать в телеграмм', url='https://t.me/domitochka5'))
        match type_of_service:
            case 'sell':
                keyboard.add(InlineKeyboardButton('Как работает продажа?', url='https://domitochka.pro/prodazhanedvizhimoztipodkluzh'))
            case 'buy':
                keyboard.add(InlineKeyboardButton('Почему лучше с нами?', url='https://domitochka.pro/poiskdomamechti'))
            case 'docs':
                keyboard.add(InlineKeyboardButton('Чем мы поможем?', url='https://domitochka.pro/documents'))
        keyboard.add(InlineKeyboardButton('Главное меню', callback_data='menu'))
        return keyboard

    def create_keyboard4(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Вопросов нет, отправить заявку', callback_data='services_sell_final'))
        keyboard.add(InlineKeyboardButton('Главное меню', callback_data='menu'))
        return keyboard

    def create_keyboard5(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Главное меню', callback_data='menu'))
        return keyboard


class BidRequests(BidRequestsMarkup, EmailTgSendler):
    instance=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        BidRequestsMarkup.__init__(self)
        EmailTgSendler.__init__(self)


    def services(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        to_del = [send_image(chat_id, './content/services/services.jpg', 'Полное описание услуг')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard1()))
        update_msg_to_del(chat_id, user_id, to_del)


    def services_sell(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        type_of_service = cache_storage.get_value(user_id, chat_id, 'type_of_service')
        match type_of_service:
            case 'sell':
                to_del = [send_image(chat_id, path='./content/services/services.jpg')]
                to_del.append(bot.send_message(chat_id, 'Краткое описание помощи при продаже', reply_markup=self.create_keyboard2()))
            case 'buy':
                to_del = [send_image(chat_id, path='./content/services/services.jpg')]
                to_del.append(bot.send_message(chat_id, 'Краткое описание помощи с покупкой', reply_markup=self.create_keyboard2()))
            case 'docs':
                to_del = [send_image(chat_id, path='./content/services/services.jpg')]
                to_del.append(bot.send_message(chat_id, 'Краткое описание помощи с документами', reply_markup=self.create_keyboard2()))
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard3(chat_id, user_id)))
        update_msg_to_del(chat_id, user_id, to_del)


    @bot.message_handler(content_types=['contact'])
    def services_sell_handler(self, message:Message, state:StateContext) -> UserBid:
        chat_id, user_id = message.chat.id, message.from_user.id
        state.set(UserStates.waiting_question_services)
        del_msg(chat_id, user_id)
        with suppress(Exception):
            bid = UserBid.from_message(message)
            UserBid.save_bid(bid, chat_id, user_id)
        with suppress(Exception):
            bot.delete_message(chat_id, message.message_id)
        to_del=[send_image(chat_id, './content/services/services.jpg', 'У вас есть какие-нибудь дополнительные вопросы ?', kwargs=ReplyKeyboardRemove())]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard4(chat_id)))
        update_msg_to_del(chat_id, user_id, to_del)


    @bot.message_handler(state=UserStates.waiting_question_services)
    def services_bid_send(self, message:Message|None, chat_id:int|str|None, user_id:int|str|None) -> None:
        with suppress(Exception):
            chat_id, user_id = message.chat.id, message.from_user.id
            question = message.text
        try:
            bid = UserBid.load_user_bid(chat_id, user_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            create_msg_thread(chat_id, user_id, 'Упс, произошла ошибка, попробуйте обновить форму или свяжитесь со специалистом')
            return self.services_sell(chat_id, user_id)
        type_of_service = cache_storage.get_value(user_id, chat_id, 'type_of_service')
        del_msg(chat_id, user_id)
        to_del = [send_image(chat_id, './content/services/services.jpg', 'Спасибо, мы скоро с вами свяжемся')]
        self.register_bid_email_tg(bid, type_of_service, question or None)
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard5()))
        update_msg_to_del(chat_id, user_id, to_del)