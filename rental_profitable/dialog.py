from abc import ABC
from decimal import Decimal
import time
from bot_instance import bot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from fsm import cache_storage, UserStates
from utils.utils import del_msg, run_in_thread, update_msg_to_del
from utils.middlewares import LogExceptionMiddlewareMeta
from telebot.states.sync.context import StateContext
from rental_profitable.functions import CalculatingRentProfitable


class RentProfitableTypes(ABC):
    def __init__(self):
        super().__init__()


    def create_keyboard1(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('▶Начать', callback_data='r_property_appreciation'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        keyboard.row(InlineKeyboardButton('🤔 Как это работает?¿?', url='https://vc.ru/u/1529738-pashtet-medved/803809-dohodnyy-analiz-ceny-kak-prodat-po-maksimumu-kommercheskuyu-nedvizhimost-i-zhile-pod-arendu'))
        return keyboard


    def create_keyboard2(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.add(InlineKeyboardButton('⚒ В главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard3(self) -> InlineKeyboardMarkup:
        # sourcery skip: class-extract-method
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='back_to_rpa'), InlineKeyboardButton('🧨 Рестарт', callback_data='r_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard4(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('🔴 Доля', callback_data='r_share'), InlineKeyboardButton('🟠 1 комн', callback_data='r_1room'), InlineKeyboardButton('🟡 2 комн', callback_data='r_2room'))
        keyboard.row(InlineKeyboardButton('🟢 3 комн', callback_data='r_3room'), InlineKeyboardButton('🔵 4 комн', callback_data='r_4room'), InlineKeyboardButton('🟣 5 и 5+ комнаты', callback_data='r_5room'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='r_back_to_raa'), InlineKeyboardButton('🧨 Рестарт', callback_data='r_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard5(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='back_to_rnor'), InlineKeyboardButton('🧨 Рестарт', callback_data='r_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard6(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='back_to_rfp'), InlineKeyboardButton('🧨 Рестарт', callback_data='r_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard7(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='back_to_rrp'), InlineKeyboardButton('🧨 Рестарт', callback_data='r_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard8(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.by'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='back_to_rmc'), InlineKeyboardButton('🧨 Рестарт', callback_data='r_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


class RentProfitableErrors(RentProfitableTypes, ABC, meta_class=LogExceptionMiddlewareMeta):
    def __init__(self):
        RentProfitableTypes.__init__(self)
        ABC.__init__(self)


    def property_appreciation_error(self, message:Message, state:StateContext) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        state.set(UserStates.waiting_price_of_house_for_rent)
        del_msg(chat_id, user_id)
        to_del = [bot.send_message(chat_id, ' Упс, Хьюстон, у нас проблемы. Неверный формат ввода, пожалуйста, повторите ввод.\n Или обратитесь к специалисту.', reply_to_message_id=message.id)]
        to_del.append(bot.send_message(chat_id, 'Введите оценку стоимости недвижимости $/м²'))
        to_del.append(bot.send_message(message.chat.id, 'Меню:', reply_markup=self.create_keyboard1()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    def property_appreciation_error_big_price(self, message:Message, state:StateContext) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        state.set(UserStates.waiting_price_of_house_for_rent)
        del_msg(chat_id, user_id)
        to_del = [bot.send_message(chat_id, 'Я думаю у вас есть что обсудить со специалистом.\n Учитывая низкую ликвидность объектов такого рода, я не смогу дать точную оценку. \n Вы можете оставить заявку или позвонить на круглосуточную линию, если вам нужен индивидуальный подход.')]
        to_del.append(bot.send_message(chat_id, 'Или можете продолжить, если указали неверную сумму.\n Для этого введите оценку стоимости недвижимости $/м², ещё раз.'))
        to_del.append(bot.send_message(message.chat.id, 'Меню:', reply_markup=self.create_keyboard2()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    def apartment_area_error(self, message:Message, state:StateContext) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_apartment_area_for_rent)
        to_del = [bot.send_message(chat_id, ' Упс, Хьюстон, у нас проблемы. Неверный формат ввода, пожалуйста, повторите ввод.')]
        to_del.append(bot.send_message(chat_id, 'Введите площадь квартиры м²'))
        to_del.append(bot.send_message(chat_id, 'Меню:', reply_markup=self.create_keyboard3()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    def forecast_period_error(self, message:Message, state:StateContext) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_forcast_period_for_rent)
        to_del = [bot.send_message(chat_id, 'Упс, Хьюстон, у нас проблемы. Неверный формат ввода, пожалуйста, повторите ввод.', reply_to_message_id=message.id)]
        to_del.append(bot.send_message(message.chat.id, 'Введите срок прогнозирования (количество лет)'))
        to_del.append(bot.send_message(message.chat.id, 'Меню:', reply_markup=self.create_keyboard5()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    def rental_price_error(self, message:Message, state:StateContext) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        state.set(UserStates.waiting_rental_price_for_rent)
        to_del = [bot.send_message(chat_id, ' Упс, Хьюстон, у нас проблемы. \n Неверный формат ввода, пожалуйста, повторите ввод.')]
        to_del.append(bot.send_message(chat_id, 'Введите ставку арендной платы $/месяц'))
        to_del.append(bot.send_message(chat_id, 'Меню:', reply_markup=self.create_keyboard6()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    def maintenance_cost_error(self, message:Message, state:StateContext) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_maintance_cost_for_rent)
        to_del = [bot.send_message(chat_id, ' Упс, Хьюстон, у нас проблемы. Возникла ошибка, пожалуйста, повторите ввод.')]
        to_del.append(bot.send_message(chat_id, 'Введите затраты на содержание $ в год, учтите необходимость периодического космитического ремонта ремонта и обновление устаревшей техники'))
        to_del.append(bot.send_message(chat_id, 'Меню:', reply_markup=self.create_keyboard7()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


class RentProfitable(RentProfitableTypes, RentProfitableErrors, meta_class=LogExceptionMiddlewareMeta):
    instance=None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self) -> None:
        super().__init__()


    def send_greeting(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        with open('./content/rent/hello.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Привет, я телеграм-бот, который рассчитывает выгодность сдачи квартиры по доходному методу. Я буду задавать вам несколько вопросов, а потом покажу вам результаты. Вы можете начать сначала, если захотите, или перейти на мой тг аккаунт или сайт, если заинтереваны')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard1()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_started')


    def property_appreciation(self, message:Message, state:StateContext) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_price_of_house_for_rent)
        with open('./content/rent/price.jpg', 'rb') as img:
            to_del = [bot.send_photo(chat_id, img, caption='Введите оценку стоимости недвижимости. Если вы её не знаете, то можете воспользоваться \n функцией рассчёта рыночной стоимости.')]
        to_del.append(bot.send_message(message.chat.id, 'Меню:', reply_markup=self.create_keyboard1()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    @bot.message_handler(state=UserStates.waiting_price_of_house_for_rent)
    def prop_ap_hand(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        try:
            message.text = message.text.replace(',', '.')
            r_answer = Decimal(message.text)
            if not Decimal('1') <= r_answer <= Decimal('250000'):
                return self.property_appreciation_error_big_price(message)
            if '.' in message.text and len(message.text.split('.')[-1]) > 2:
                return self.property_appreciation_error(message)
            if message.text.startswith('0') and message.text != '0':
                return self.property_appreciation_error(message)
            if message.text.startswith('-'):
                return self.property_appreciation_error(message)
        except ValueError:
            return self.property_appreciation_error(message)
        cache_storage.set_value(user_id, chat_id, 'r_property_appreciation', Decimal(r_answer))
        return self.apartment_area(chat_id, user_id)


    def apartment_area(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        state.set(UserStates.waiting_apartment_area_for_rent)
        del_msg(chat_id, user_id)
        with open('./content/rent/area.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Введите площадь квартиры м²')]
        to_del.append(bot.send_message(chat_id, 'Меню:', reply_markup=self.create_keyboard3()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    @bot.message_handler(state = UserStates.waiting_apartment_area_for_rent)
    def ap_ar_hand(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        try:
            message.text = message.text.replace(',', '.')
            r_answer = float(message.text)
            if not 1 <= r_answer <= 9999:
                return self.apartment_area_error(message)
            if '.' in message.text and len(message.text.split('.')[-1]) > 2:
                return self.apartment_area_error(message)
            if message.text.startswith('0') and message.text != '0':
                return self.apartment_area_error(message)
            if message.text.startswith('-'):
                return self.apartment_area_error(message)
        except ValueError:
            return self.apartment_area_error(message)
        cache_storage.set_value(user_id, chat_id, 'r_apartment_area', r_answer)
        self.number_of_rooms(chat_id, user_id)


    def number_of_rooms(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        with open('./content/rent/rooms.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Выберите количество комнат в квартире.')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard4()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    def forecast_period(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_forcast_period_for_rent)
        with open('./content/rent/forecast.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, 'Введите срок прогнозирования (количество лет)')]
        to_del.append(bot.send_message(chat_id, 'Меню:', reply_markup=self.create_keyboard5()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    @bot.message_handler(state=UserStates.waiting_forcast_period_for_rent)
    def r_for_per_hand(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        try:
            message = message.text.replace('-', '')
            message.text = message.text.split('.')[0].split(',')[0]
            message.text = message.text.lstrip('0')
            r_answer = int(message.text, 10)
            if not (0 <= r_answer <= 99):
                return self.forecast_period_error(message)
        except ValueError:
            return self.forecast_period_error(message)
        cache_storage.set_value(user_id, chat_id, 'r_forecast_period', r_answer)
        return self.rental_price(chat_id, user_id)


    def rental_price(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_rental_price_for_rent)
        with open('./content/rent/income.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Введите ставку арендной платы $/месяц')]
        to_del.append(bot.send_message(chat_id, 'Меню:', reply_markup=self.create_keyboard6()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    @bot.message_handler(state = UserStates.waiting_rental_price_for_rent)
    def r_rent_price_hand(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        try:
            message.text = message.text.replace(',', '.')
            r_answer = float(message.text)
            if not 1 <= r_answer <= 9999:
                return self.property_appreciation_error(message)
            if '.' in message.text and len(message.text.split('.')[-1]) > 2:
                return self.property_appreciation_error(message)
            if message.text.startswith('-'):
                return self.property_appreciation_error(message)
        except ValueError:
            return self.property_appreciation_error(message)
        cache_storage.set_value(user_id, chat_id, 'r_rental_price', r_answer)
        self.maintenance_cost(chat_id, user_id)


    def maintenance_cost(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_maintance_cost_for_rent)
        with open('./content/rent/costs.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Введите затраты на содержание $ в год, учтите необходимость периодического космитического ремонта ремонта и обновление устаревшей техники')]
        to_del.append(bot.send_message(chat_id, 'Меню:', reply_markup=self.create_keyboard7()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')


    @bot.message_handler(state = UserStates.waiting_maintance_cost_for_rent)
    def r_the_end(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        if not message.text:
            return self.maintenance_cost_error(message)
        try:
            message.text = message.text.replace(',', '.')
            r_answer = float(message.text)
            if not 1 <= r_answer <= 9999:
                return self.maintenance_cost_error(message)
            if '.' in message.text and len(message.text.split('.')[-1]) > 2:
                return self.maintenance_cost_error(message)
            if message.text.startswith('0') and message.text != '0':
                return self.maintenance_cost_error(message)
            if message.text.startswith('-'):
                return self.maintenance_cost_error(message)
        except ValueError:
            return self.maintenance_cost_error(message)
        cache_storage.set_value(user_id, chat_id, 'r_maintenance_costs', r_answer)
        self.send_results(chat_id, user_id)



    def send_results(self, chat_id:int, user_id:int) -> None:
        # sourcery skip: extract-method, hoist-similar-statement-from-if
        # sourcery skip: hoist-statement-from-if, inline-immediately-returned-variable
        # sourcery skip: move-assign-in-block, remove-redundant-fstring
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'completed')
        CalculatingRentProfitable(chat_id, user_id).rent_results()
        results = cache_storage.get_values(user_id, chat_id)
        if results['r_is_profitable']:
            message1 = f"**Оценка, с учётом того, что за планируемый срок сдачи цена не изменится.** \n\n Настоящая стоимость квартиры по рыночному методу: {int(results['r_property_appreciation'])} $.\n"
            message1 += f"Это стоимость, которую вы можете получить от продажи квартиры сейчас, учитывая ожидаемую рыночную стоимость и оценку стоимости недвижимости."
            message2 = f"Планируемый доход через {int(results['r_forecast_period'])} лет с учетом продажи квартиры: {int(results['r_present_apartment_value'], 500)} $.\n"
            message2 += f"Это доход, который вы можете получить от сдачи квартиры в аренду за {int(results['r_forecast_period'])} лет и продажи ее по истечении этого срока, учитывая дисконтирование, инфляцию, ставку вакансии и затраты на содержание."
            message3 = f"\n Сдача квартиры в аренду выгодна.\n"
            message3 += f"Это значит, что планируемый доход от сдачи и продажи квартиры больше, чем настоящая стоимость квартиры. Вы можете получить дополнительный доход от аренды квартиры, пока она растет в цене."
            with open('./content/rent/result.jpg', 'rb') as img1:
                to_del = [bot.send_photo(chat_id, img1, caption=message1 + message2 + message3, parse_mode='Markdown')] 
        else:
            message1 = f"**Оценка, с учётом того, что за планируемый срок сдачи цена не изменится.** \n\n Настоящая стоимость квартиры по рыночному методу: {int(results['r_property_appreciation'])} $.\n"
            message1 += f"Это стоимость, которую вы можете получить от продажи квартиры сейчас, учитывая ожидаемую рыночную стоимость и оценку стоимости недвижимости."
            message2 = f"Планируемый доход через {int(results['r_forecast_period'])} лет с учетом продажи квартиры: {int(results['r_present_apartment_value'], 500)} $.\n"
            message2 += f"Это доход, который вы можете получить от сдачи квартиры в аренду за {int(results['r_forecast_period'])} лет и продажи ее по истечении этого срока, учитывая дисконтирование, инфляцию, ставку вакансии и затраты на содержание."
            message3 = f"\n Сдача квартиры в аренду невыгодна.\n"
            message3 += f"Это значит, что планируемый доход от сдачи и продажи квартиры меньше, чем настоящая стоимость квартиры. Вы можете потерять часть своего капитала, если будете сдавать квартиру в аренду, вместо того, чтобы продать ее сейчас."
            with open('./content/rent/result.jpg', 'rb') as img1:
                to_del = [bot.send_photo(chat_id, img1, caption=message1 + message2 + message3, parse_mode='Markdown')]
        if results['r_is_profitable_up']:
            message1 = f"**Оценка, с учётом того, что за планируемый срок сдачи цены на недвижимость будут расти.** \n\n"
            message2 = f"Планируемый доход через {int(results['r_forecast_period'])} лет с учетом продажи квартиры: {int(results['r_present_apartment_value_up'], 500)} $.\n"
            message2 += f"Это доход, который вы можете получить от сдачи квартиры в аренду за {int(results['r_forecast_period'])} лет и продажи ее по истечении этого срока. Здесь также учитываются дисконтирование, инфляцию, ставка вакансии и затраты на содержание."
            message3 = f"\n Сдача квартиры в аренду выгодна.\n"
            message3 += f"Это значит, что планируемый доход от сдачи и продажи квартиры больше, чем настоящая стоимость квартиры. Вы можете получить дополнительный доход от аренды квартиры, пока она растет в цене."
            to_del.append(bot.send_message(chat_id, message1 + message2 + message3, parse_mode='Markdown'))
        else:
            message1 = f"**Оценка, с учётом того, что за планируемый срок сдачи цены на недвижимость будут расти.** \n\n"
            message2 = f"Планируемый доход через {int(results['r_forecast_period'])} лет с учетом продажи квартиры: {int(results['r_present_apartment_value_up'], 500)} $.\n"
            message2 += f"Это доход, который вы можете получить от сдачи квартиры в аренду за {int(results['r_forecast_period'])} лет и продажи ее по истечении этого срока, учитывая дисконтирование, инфляцию, ставку вакансии и затраты на содержание."
            message3 = f"\n Сдача квартиры в аренду невыгодна.\n"
            message3 += f"Это значит, что планируемый доход от сдачи и продажи квартиры меньше, чем настоящая стоимость квартиры. Вы можете потерять часть своего капитала, если будете сдавать квартиру в аренду, вместо того, чтобы продать ее сейчас."
            to_del.append(bot.send_message(chat_id, message1 + message2 + message3, parse_mode='Markdown'))
        if results['r_is_profitable_down']:
            message1 = f"**Оценка, с учётом того, что за планируемый срок сдачи цены на недвижимость будут падать.** \n\n"
            message2 = f"Планируемый доход через {int(results['r_forecast_period'])} лет с учетом продажи квартиры: {int(results['r_present_apartment_value_down'], 500)} $.\n"
            message2 += f"Это доход, который вы можете получить от сдачи квартиры в аренду за {int(results['r_forecast_period'])} лет и продажи ее по истечении этого срока. Всё учтено."
            message3 = f"\n Сдача квартиры в аренду выгодна.\n"
            message3 += f"Это значит, что планируемый доход от сдачи и продажи квартиры больше, чем настоящая стоимость квартиры. Вы можете получить дополнительный доход от аренды квартиры, пока она растет в цене."
            to_del.append(bot.send_message(chat_id, message1 + message2 + message3, parse_mode='Markdown'))
        else:
            message1 = f"**Оценка, с учётом того, что за планируемый срок сдачи цены на недвижимость будут падать.** \n\n"
            message2 = f"Планируемый доход через {int(results['r_forecast_period'])} лет с учетом продажи квартиры: {int(results['r_present_apartment_value_down'], 500)} $.\n"
            message2 += f"Это доход, который вы можете получить от сдачи квартиры в аренду за {int(results['r_forecast_period'])} лет и продажи ее по истечении этого срока, учитывая дисконтирование, инфляцию, ставку вакансии и затраты на содержание."
            message3 = f"\n Сдача квартиры в аренду невыгодна.\n"
            message3 += f"Это значит, что планируемый доход от сдачи и продажи квартиры меньше, чем настоящая стоимость квартиры. Вы можете потерять часть своего капитала, если будете сдавать квартиру в аренду, вместо того, чтобы продать ее сейчас."
            to_del.append(bot.send_message(chat_id, message1 + message2 + message3, parse_mode='Markdown'))
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard8()))
        update_msg_to_del(chat_id, user_id, to_del) 


    @run_in_thread()
    def restart(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        to_del = [bot.send_message(chat_id, 'Перезапуск функции рассчёта')]
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'r_in_progress')
        time.sleep(2)
        self.send_greeting(chat_id, user_id)