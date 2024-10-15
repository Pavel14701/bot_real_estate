# импортируем библиотеки
import telebot, time, threading, pickle, re, time, os, math, random
import telebot, schedule , requests, datetime, g4f, smtplib, matplotlib.pyplot as plt
import pandas as pd, numpy as np, statistics
from sqlalchemy import text
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telebot.handler_backends import State, StatesGroup
from decimal import Decimal
from g4f.client import Client
from email.mime.text import MIMEText
from dotenv import load_dotenv
from db import CacUserData, User, StreetName, create_tables
from fsm import bot, state_storage
load_dotenv()

Session, Session_streets = create_tables()



def get_state(user_id):
    return state_storage.get_value(str(user_id))

def update_state(user_id, state):
    state_storage.set_value(str(user_id), state)

def reset_state(user_id):
    state_storage.delete_value(str(user_id))


class EmailSender:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.smtp_user = os.getenv('MAIL')
        self.smtp_password = os.getenv('MAIL_PASSWORD')
        
    def send_email(self, subject, message, to_email):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = to_email
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_user, self.smtp_password)
        server.sendmail(self.smtp_user, to_email, msg.as_string())
        server.quit()



BASE_VALUE = 40 # базовая величина в BYN
CURRENCY_API = 'https://api.nbrb.by/exrates/rates?periodicity=0'





# ГЛАВНОЕ МЕНЮ
def create_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("🤖 Кузя - ваш помошник на базе AI", callback_data="kuzia_chatbotai"))
    keyboard.add(telebot.types.InlineKeyboardButton("🔍 Анализ рыночной цены", callback_data="price"))
    keyboard.add(telebot.types.InlineKeyboardButton("🧮 Калькулятор риэлторских услуг", callback_data="calc"))
    keyboard.add(telebot.types.InlineKeyboardButton("💵 Анализ прибыльности сдачи квартиры в аренду", callback_data="rent"))
    """
    #keyboard.add(telebot.types.InlineKeyboardButton("🧠 Аналитика", callback_data="analytics"))
    #keyboard.add(telebot.types.InlineKeyboardButton("Подбор квартиры по характеристикам", callback_data="search"))
    """
    keyboard.add(telebot.types.InlineKeyboardButton("😎 Услуги", callback_data="services"))
    return keyboard

@bot.message_handler(commands=["start"])
def menu1(message):
    uid = message.chat.id
    chat_id = uid
    state_storage.set_value(f'reminder_states:{chat_id}', 'completed')
    nick1 = message.from_user.first_name
    nick2 = message.from_user.last_name
    start_time = datetime.datetime.now()
    user = User(uid = uid,
                nick1 = nick1,
                nick2 = nick2,
                start_time = datetime.datetime.now()
                )
    with Session() as session_start:
        if not session_start.query(User).filter_by(uid=uid).first():
            session_start.add(user)
            session_start.commit()
        user = CacUserData(user_id=uid)
        if not session_start.query(CacUserData).filter_by(user_id=uid).first():
            session_start.add(user)
            session_start.commit()
    photo_main = bot.send_photo(uid, open("C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\hello.jpg", "rb"))
    message_main1 = bot.send_message(uid, f"Привет {nick1} {nick2}, меня зовут Кузя и я помогу вам с решением различных задач, связанных с недвижимостью. Я могу проанализировать прибыльность сдачи квартиры в аренду, оценить рыночную стоимость и рассчитать стоимость риэлторских услуг.")
    message_main2 = bot.send_message(uid, "Выберите один из вариантов:", reply_markup=create_keyboard())
    state_storage.set_value(f'main_del:{chat_id}', message_main2.message_id)


def menu(chat_id):
    reset_state(chat_id)
    msgs_del = ['ai_del', 'cf_cur_sel_del', 'cac_ccr_del', 'cac_region_choice_del', 'cac_fin_street_choice_del', 'cac_chn_del',
                    'cac_ctoh_del', 'cac_ctm_del', 'cac_ctb_del', 'cac_ctp_del', 'cac_caoh_del', 'cac_cnore_del',
                    'cac_cta_del', 'cac_cpf_del', 'r_ar_del', 'r_ar_er_del', 'r_for_del', 'r_for_er_del',
                    'r_rent_del', 'r_rent_er_del', 'r_mcost_del', 'r_mcost_er_del', 'r_rsr_del', 'r_greet_del', 'services_final_del', 'serv_sell_handler_del',
                    'services_sell_dell']
    for msg in msgs_del:
        try:
            msg_del = state_storage.get_value(f'{msg}:{chat_id}')
            try:
                bot.delete_message(chat_id, msg_del)
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except:
            pass
    photo_main = bot.send_photo(chat_id, open("C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\hello.jpg", "rb"))
    state_storage.set_value(f'reminder_states:{chat_id}', 'completed')
    with Session() as session_name:
        user = session_name.query(User).filter_by(uid=chat_id).first()
        nick1 = user.nick1
        nick2 = user.nick2
    message_main1 = bot.send_message(chat_id, f"Привет {nick1} {nick2}, меня зовут Кузя и я помогу вам с решением различных задач, связанных с недвижимостью. Я могу проанализировать прибыльность сдачи квартиры в аренду, оценить рыночную стоимость и рассчитать стоимость риэлторских услуг.")
    message_main2 = bot.send_message(chat_id, "Выберите один из вариантов:", reply_markup=create_keyboard())
    state_storage.set_value(f'main_del:{chat_id}', message_main2.message_id)

def send_greeting_cac(chat_id):
    del_mes = state_storage.get_value(f'main_del:{chat_id}')
    try:
        bot.delete_message (chat_id, del_mes)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    message_greeting = bot.send_message(chat_id, 'Так, вы хотите узнать рыночную стоимость квартиры. Учтите, что я могу рассчитать только примерный диапазон,\n для точной оценки свяжитесь с нашим специалистом. Это бесплатно. Для рассчёёта мне нужно задать вам несколько вопросов, а потом покажу вам результаты. Вы не против ?\n Кстати, я запомню все ваши ответы и смогу в будущем рассчитать стоимость, потому что они не стоят на месте, а постоянно меняются.')
    message_greet = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_cac1())
    state_storage.set_value(f'cac_greet_del:{chat_id}', message_greet.message_id)

def create_keyboard_cac1():
    keyboard1cac = types.InlineKeyboardMarkup()
    keyboard1cac.row(types.InlineKeyboardButton('🔍 Пожалуй начнём', callback_data='cac_minsk_region_entry'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    keyboard1cac.add(types.InlineKeyboardButton('💼 Расчёт по сохранёным параметрам', callback_data='cac_calculate_results'))
    keyboard1cac.add(types.InlineKeyboardButton('Как это работает ?¿?', url='https://vc.ru/u/1529738-pashtet-medved/800356-sravnitelnyy-metod-ocenki-nedvizhimosti-kak-zarabotat-na-prodazhe-svoey-nedvizhimosti-v-usloviyah-krizisa'))
    keyboard1cac.row(types.InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт', url='https://domitochka.pro'))
    return keyboard1cac




# Создаём функцию для опроса о районе Минска
def cac_minsk_region_choice(chat_id):
    msg_del = state_storage.get_value(f'cac_street_del:{chat_id}')
    try:
        bot.delete_message(chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    greet_del = state_storage.get_value(f'cac_greet_del:{chat_id}')
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\region.jpg', 'rb') as img:
        bot.send_photo(chat_id, img, caption='Укажите район Минска, в котором расположен оцениваемый объект.')
    try:
        bot.delete_message (chat_id, greet_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    cmrc = bot.send_message(chat_id, 'Выберите из списка', reply_markup=create_keyboard_cac2())
    state_storage.set_value(f'cac_region_choice_del:{chat_id}', cmrc.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_started')

def create_keyboard_cac2():
    keyboard2cac = types.InlineKeyboardMarkup()
    keyboard2cac.row(types.InlineKeyboardButton('🐦‍⬛ Центральный', callback_data='cac_centr'), types.InlineKeyboardButton('🐦‍⬛ Фрунзенский', callback_data='cac_frunz'))
    keyboard2cac.row(types.InlineKeyboardButton('🐦‍⬛ Ленинский', callback_data='cac_lenin'), types.InlineKeyboardButton('🐦‍⬛ Московский', callback_data='cac_moscow'))
    keyboard2cac.row(types.InlineKeyboardButton('🐦‍⬛ Заводской', callback_data='cac_zavod'), types.InlineKeyboardButton('🐦‍⬛ Первомайский', callback_data='cac_firstmay'))
    keyboard2cac.row(types.InlineKeyboardButton('🐦‍⬛ Октябрьский', callback_data='cac_october'), types.InlineKeyboardButton('🐦‍⬛ Советский', callback_data='cac_sovet'))
    keyboard2cac.add(types.InlineKeyboardButton('🐦‍⬛ Партизанский', callback_data='cac_partiz'))
    keyboard2cac.row(types.InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт', url='https://domitochka.pro'))
    keyboard2cac.add(types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard2cac

# Создаём функцию для опроса об улице
def cac_minsk_street_choice(chat_id):
    msgs_del = ['cac_fin_street_choice_del', 'cac_region_choice_del']
    for msg_del in msgs_del:
        try:
            mes_del = state_storage.get_value(f'{msg_del}:{chat_id}')
            try:
                bot.delete_message (chat_id, mes_del)
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except:
            pass
    with open("C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\street_choice.jpg", 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Введите улицу, на которой находится оцениваемый объект.')
    cmsc = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_cac3())
    state_storage.set_value(f'cac_street_del:{chat_id}', cmsc.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')
    update_state(chat_id, 'result_street_choice')

def create_keyboard_cac3():
    keyboard3cac = types.InlineKeyboardMarkup()
    keyboard3cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cmrc'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    keyboard3cac.add(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    return keyboard3cac

# создаем функцию для отправки клавиатуры с выбором улицы
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'result_street_choice')
def cac_final_street_choice(message):
    chat_id = message.chat.id
    mes_del = state_storage.get_value(f'cac_street_del:{chat_id}')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    state_storage.set_value(f'chosen_street_name:{chat_id}', message.text)
    chosen_street_name = state_storage.get_value(f'chosen_street_name:{chat_id}')
    street_list = []
    with Session_streets() as session_streets:
        street_names = session_streets.query(StreetName).all()
    if not message.text:
        cac_street_choice_error(chat_id)
        return
    for street in street_names:
        pattern = chosen_street_name
        if re.search(pattern, street.street_name, re.IGNORECASE):
            street_list.append(street.street_name)
    if street_list:
        with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\bd.jpg', 'rb') as img1:
            bot.send_photo(message.chat.id, img1, caption=f'Вы ввели {chosen_street_name}. По результатам сравнения с базой данных нашлось {len(street_list)} совпадений.')
        keyboard4cac = telebot.types.InlineKeyboardMarkup()
        for street in street_list:
            keyboard4cac.add(telebot.types.InlineKeyboardButton(f'🔐 {street}', callback_data=f'street_{street}'))
        keyboard4cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cmsc'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        keyboard4cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        cfsc = bot.send_message(message.chat.id, 'Выберите улицу из списка:', reply_markup=keyboard4cac)
        state_storage.set_value(f'cac_fin_street_choice_del:{chat_id}', cfsc.message_id)
    else:
        cac_street_choice_error(chosen_street_name, chat_id)

# Создаём функцию обработки ошибок в функции ввода улицы
def cac_street_choice_error(chosen_street_name, chat_id):
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\no_bd.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption=f'К сожалению, я не нашел улицу с названием {chosen_street_name} в базе даннных.')
    bot.send_message(chat_id, 'Пожалуйста, повторите ввод или свяжитесь со специалистом.')
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')
    cac_minsk_street_choice(chat_id)

# Создаём функцию ввода номера дома
def cac_house_number(chat_id):
    msgs_del = ['cac_ctoh_del', 'cac_fin_street_choice_del']
    for mes_del in msgs_del:
        try:
            msg_del = state_storage.get_value(f'{mes_del}:{chat_id}')
            try:
                bot.delete_message (chat_id, msg_del)
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except:
            pass
    update_state(chat_id, 'waiting_for_type_of_house')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\numb_h.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Введите номер дома')
    chn = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_cac4())
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')
    state_storage.set_value(f'cac_chn_del:{chat_id}', chn.message_id)

def create_keyboard_cac4():
    keyboard5cac = types.InlineKeyboardMarkup()
    keyboard5cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cmsc'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    keyboard5cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    return keyboard5cac

# Создаём функцию ввода типа дома
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'waiting_for_type_of_house')
def cac_type_of_house(message):
    chat_id = message.chat.id
    msgs_del = ['cac_ctp_del', 'cac_ctb_del', 'cac_ctm_del', 'cac_caoh_del', 'cac_chn_del']
    for msg in msgs_del:
        try:
            mes_del = state_storage.get_value(f'{msg}:{chat_id}')
            try:
                bot.delete_message(chat_id, mes_del)
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except:
            pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick.jpg', 'rb') as img2, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\mon.jpg', 'rb') as img3:
        bot.send_photo(chat_id, img1, caption='Панельные дома — здания из железобетонных панелей, собранных на месте. Внешние стены — многослойные, с утеплителем; внутренние — однослойные. Различаются по размеру и материалам.')
        bot.send_photo(chat_id, img2, caption='Кирпичный дом — это здание, построенное из кирпича, материала с высокой прочностью и долговечностью. Стены могут быть полнотелыми или пустотелыми, с различными отделочными вариантами. Кирпичные дома ценятся за их теплоизоляцию и эстетику.')
        bot.send_photo(chat_id, img3, caption='Монолитный дом — это здание с бесшовным каркасом, отлитым из бетона поэтажно. Отсутствие стыков делает его прочным и устойчивым к погодным условиям.')
    bot.send_message(chat_id, 'Выберите тип дома из списка')
    ctoh = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_cac6())
    state_storage.set_value(f'cac_ctoh_del:{chat_id}', ctoh.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')

def create_keyboard_cac6():
    keyboard6cac = types.InlineKeyboardMarkup()
    keyboard6cac.row(types.InlineKeyboardButton('🏢 Панельный', callback_data='cac_panel'), types.InlineKeyboardButton('🧱 Кирпичный', callback_data='cac_brick'), types.InlineKeyboardButton('🏛 Монолитный', callback_data='cac_monolith'))
    keyboard6cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard6cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_chn'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard6cac



# Расширение опроса типа дома панель
def cac_type_panel(chat_id):
    mes_del = state_storage.get_value(f'cac_ctoh_del:{chat_id}')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel\\chruzh1.jpg', 'rb') as img1,\
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel\\chruzh2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Хрущёвки — это типовые многоквартирные дома, которые были массово построены в СССР с 1956 по 1974 год. Они получили своё название в честь Никиты Хрущёва, который инициировал их строительство как решение проблемы нехватки жилья после Второй мировой войны. Хрущёвки обычно имеют 4-5 этажей, хотя встречаются и 2-3, а также 8-9 этажные варианты. Эти дома отличаются простой и функциональной архитектурой, а квартиры в них имеют относительно небольшие размеры"),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel\\brezh1.jpg', 'rb') as img1,\
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel\\brezh2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Брежневки — это типовые жилые дома, которые строились в СССР с 1964 по 1985 год. Они названы в честь Леонида Брежнева и являются улучшенной версией хрущёвок. Брежневки представляют собой панельные, блочные или кирпичные дома, которые отличаются более продуманной планировкой и большей площадью квартир. В отличие от хрущёвок, в брежневках иногда есть лифты, присутствуют балконы или лоджии, а также улучшенная звуко и теплоизоляция"),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel\\standart1.jpg', 'rb') as img1,\
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel\\standart2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Дома стандартного проекта в Минске и других городах бывшего СССР — это многоэтажные здания, в основном из железобетонных панелей, хотя встречаются и кирпичные варианты. Типичные дома имеют от 5 до 12 этажей, с преобладанием 9-этажных конструкций. Квартиры разнообразны по размеру и могут включать от 1 до 4 комнат, оборудованы встроенными шкафами и мусоропроводами. Стандартная высота потолков составляет 2,5 метра. В большинстве домов установлены лифты, а на первых этажах расположены магазины и другие объекты инфраструктуры."),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel\\upgrade1.jpg', 'rb') as img1,\
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\panel\\upgrade2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Дома с улучшенными планировками — это современные жилые здания с повышенным комфортом и энергоэффективностью. Они отличаются качественными материалами, улучшенной тепло- и звукоизоляцией, разнообразной планировкой, большими площадями и эстетичными фасадами. Высота потолков 2.5 - 2.7 метра."),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    ctp = bot.send_message(chat_id, 'Существует несколько видов панельных домов. Выберите к какому из перечисленных видов относится ваш.', reply_markup=create_keyboard_cac7())
    state_storage.set_value(f'cac_ctp_del:{chat_id}', ctp.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')


def create_keyboard_cac7():
    keyboard7cac = types.InlineKeyboardMarkup()
    keyboard7cac.row(types.InlineKeyboardButton('🏡 Хрущёвка', callback_data='cac_hrush'), types.InlineKeyboardButton('🏡 Брежневка', callback_data='cac_brezh'))
    keyboard7cac.row(types.InlineKeyboardButton('🏡 Стандартный проект', callback_data='cac_standart'), types.InlineKeyboardButton('🏡 Улучшеный проект', callback_data='cac_upgrade'))
    keyboard7cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard7cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_ctoh'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard7cac

def cac_type_brick(chat_id):
    mes_del = state_storage.get_value(f'cac_ctp_del:{chat_id}')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\stalin1.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\stalin2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="“Сталинки” — это название, данное многоквартирным домам, построенным в СССР с конца 1930-х до середины 1950-х годов, в основном в период правления Иосифа Сталина. Эти здания отличаются капитальным строением, высокими потолками, просторными квартирами и часто выполнены в стиле неоклассицизма. Высокие потолки 2.7 - 3 метра. Сталинки известны своей прочностью, качественными материалами и декоративными элементами, такими как лепнина на фасадах"),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\chruzh1.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\chruzh2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Хрущёвки — это типовые многоквартирные дома, которые были массово построены в СССР с 1956 по 1974 год. Они получили своё название в честь Никиты Хрущёва, который инициировал их строительство как решение проблемы нехватки жилья после Второй мировой войны. Хрущёвки обычно имеют 4-5 этажей, хотя встречаются и 2-3, а также 8-9 этажные варианты. Эти дома отличаются простой и функциональной архитектурой, а квартиры в них имеют относительно небольшие размеры"),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\brezh1.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\brezh2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Брежневки — это типовые жилые дома, которые строились в СССР с 1964 по 1985 год. Они названы в честь Леонида Брежнева и являются улучшенной версией хрущёвок. Брежневки представляют собой панельные, блочные или кирпичные дома, которые отличаются более продуманной планировкой и большей площадью квартир. В отличие от хрущёвок, в брежневках часто есть лифты, балконы или лоджии, а также улучшенная звукоизоляция"),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\standart1.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\standart2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Дома стандартного проекта в Минске и других городах бывшего СССР — это многоэтажные здания, в основном из железобетонных панелей, хотя встречаются и кирпичные варианты. Типичные дома имеют от 5 до 12 этажей, с преобладанием 9-этажных конструкций. Квартиры разнообразны по размеру и могут включать от 1 до 4 комнат, оборудованы встроенными шкафами и мусоропроводами. Стандартная высота потолков составляет 2,5 метра. В большинстве домов установлены лифты, а на первых этажах расположены магазины и другие объекты инфраструктуры."),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\upgrade1.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\brick\\upgrade2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Дома с улучшенными планировками — это современные жилые здания с повышенным комфортом и энергоэффективностью. Они отличаются качественными материалами, улучшенной тепло- и звукоизоляцией, разнообразной планировкой, большими площадями и эстетичными фасадами. Высота потолков 2.5 - 2.7 метра."),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    ctb =     bot.send_message(chat_id, 'Существует несколько видов панельных домов. Выберите к какому из перечисленных видов относится ваш.', reply_markup=create_keyboard8cac())
    state_storage.set_value(f'cac_ctb_del:{chat_id}', ctb.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')

def create_keyboard8cac():
    keyboard8cac = types.InlineKeyboardMarkup()
    keyboard8cac.row(types.InlineKeyboardButton('🏡 Сталинка', callback_data='cac_stalin'), types.InlineKeyboardButton('🏡 Хрущёвка', callback_data='cac_hrush'), types.InlineKeyboardButton('🏡 Брежневка', callback_data='cac_brezh'))
    keyboard8cac.row(types.InlineKeyboardButton('🏡 Улучшеный проект', callback_data='cac_upgrade'), types.InlineKeyboardButton('🏡 Стандартный проект', callback_data='cac_standart'))
    keyboard8cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard8cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_ctoh'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard8cac

def cac_type_monolith(chat_id):
    mes_del = state_storage.get_value(f'cac_ctb_del:{chat_id}')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\monolith\\mon_brick1.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\monolith\\mon_brick2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Монолитно-кирпичные многоквартирные дома — это сочетание монолитного железобетонного каркаса для прочности и устойчивости с кирпичной кладкой для отличной тепло- и звукоизоляции. Эти дома позволяют гибкую планировку пространства, включая свободные планировки и большие окна, обеспечивая комфортное проживание. Высокая долговечность, до 150 лет, и возможность реализации разнообразных архитектурных стилей делают их популярным выбором для строительства. Важной особенностью является повышенная энергоэффективность, снижающая эксплуатационные расходы."),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\monolith\\mon_block1.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\monolith\\mon_block2.jpg', 'rb') as img2:
        media = [InputMediaPhoto(img1, caption="Каркасно-блочные дома - это тип строений, где основу конструкции составляет монолитный железобетонный каркас, а стены дополнительно утепляются и закрываются блоками. Такая технология строительства позволяет создавать прочные и долговечные здания, обладающие хорошей тепло- и звукоизоляцией. Монолитный каркас отливается из бетонной массы, что обеспечивает единую бесшовную конструкцию, устойчивую к погодным явлениям и сейсмической активности. Высокие потолки, свободные планировки. Блоки, используемые для стен, могут быть изготовлены из различных материалов, таких как пеноблоки или газобетон, что добавляет дополнительные изоляционные свойства добавь характеристики планировок"),
            InputMediaPhoto(img2)]
        bot.send_media_group(chat_id, media)
    ctm = bot.send_message(chat_id, 'Существует несколько видов панельных домов. Выберите к какому из перечисленных видов относится ваш.', reply_markup=create_keyboard_cac9())
    state_storage.set_value(f'cac_ctm_del:{chat_id}', ctm.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')

def create_keyboard_cac9():
    keyboard9cac = types.InlineKeyboardMarkup()
    keyboard9cac.add(types.InlineKeyboardButton('🏡Монолитно - кирпичный', callback_data='cac_mon_brick'))
    keyboard9cac.add(types.InlineKeyboardButton('🏡Каркасно - блочный', callback_data='cac_mon_block'))
    keyboard9cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard9cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_ctoh'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard9cac

# Функция запроса возраста дома
def cac_age_of_house(chat_id):
    msgs_del = ['cac_ctm_del', 'cac_ctp_del', 'cac_ctb_del', 'cac_cnore_del']
    for msg in msgs_del:
        try:
            mes_del = state_storage.get_value(f'{msg}:{chat_id}')
            try:
               bot.delete_message (chat_id, mes_del)
            except:
                pass
        except:
            pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\age_of_house.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Введите год постройки дома')
    caoh = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard10cac())
    state_storage.set_value(f'cac_caoh_del:{chat_id}', caoh.message_id)
    update_state(chat_id, 'waiting_age_of_house')
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')

# Обработчик ввода возраста дома
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'waiting_age_of_house')
def cac_age_of_house_handler(message):
    chat_id = message.chat.id
    mes_del = state_storage.get_value(f'cac_caoh_del:{chat_id}')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    message_text = message.text
    try:
        year = int(message_text)
    except ValueError:
        bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или свяжитесь со специалистом')
        cac_age_of_house(chat_id)
    current_year = datetime.datetime.now().year
    if year >= 1900 and year <= current_year:
        bot.send_message(chat_id, f'Вы ввели {year} год. Возраст дома составляет {current_year - year} года(лет).')
        cac_age = current_year - year
        cac_number_of_rooms_entry(chat_id)
        user_id = chat_id
        state_storage.set_value(f'cac_age:{chat_id}', cac_age)
    else:
        bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или обратитесь  к специалисту')
        cac_age_of_house(chat_id)
        
def create_keyboard10cac():
    keyboard10cac = types.InlineKeyboardMarkup()
    keyboard10cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard10cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_ctoh'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard10cac
    
# Создаём функцию ввода количества комнат
def cac_number_of_rooms_entry(chat_id):
    msg_del = state_storage.get_value(f'cac_cta_del:{chat_id}')
    try:
        bot.delete_message (chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\rooms.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Сколько комнат в квартире?')
    cnore = bot.send_message(chat_id, 'Выберите вариант из списка:', reply_markup=create_keyboard11cac())
    state_storage.set_value(f'cac_cnore_del:{chat_id}', cnore.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')
    
def create_keyboard11cac():
    keyboard11cac = types.InlineKeyboardMarkup()
    keyboard11cac.row(types.InlineKeyboardButton('🔴 Доля', callback_data='cac_share'), types.InlineKeyboardButton('🟠 1 комн', callback_data='cac_1room'), types.InlineKeyboardButton('🟡 2 комн', callback_data='cac_2room'))
    keyboard11cac.row(types.InlineKeyboardButton('🟢 3 комн', callback_data='cac_3room'), types.InlineKeyboardButton('🔵 4 комн', callback_data='cac_4room'), types.InlineKeyboardButton('🟣 5 и 5+ комнаты', callback_data='cac_5room'))
    keyboard11cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard11cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_caoh'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard11cac

# Создаём функцию ввода площади
def cac_total_area(chat_id):
    update_state(chat_id, 'waiting_area_of_house')
    mes_del = state_storage.get_value(f'cac_cnore_del:{chat_id}')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\area.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Введите общую площадь квартиры')
    cta = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard12cac())
    state_storage.set_value(f'cac_cta_del:{chat_id}', cta.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')
    
# Обработчик ввода площади
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'waiting_area_of_house')
def cac_total_area_handler(message):
    chat_id = message.chat.id
    msg_del = state_storage.get_value(f'cac_cr_del:{chat_id}')
    try:
        bot.delete_message (chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    mes_del = state_storage.get_value(f'cac_cta_del:{chat_id}')
    max_area = 999
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    message_text = message.text
    try:
        message_text = message_text.replace(",", ".")
        area = float(message_text)
        area = round(area, 2)
        if area >= 1 and area <= max_area:
            bot.send_message(chat_id, f'Вы ввели {area} м².')
            user_id = chat_id
            state_storage.set_value(f'area:{chat_id}', area)
            cac_repair(chat_id)
        else:
            bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или обратитесь  к специалисту')
            cac_total_area(chat_id)
    except ValueError:
        bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или обратитесь  к специалисту')
        cac_total_area(chat_id)

def create_keyboard12cac():
    keyboard12cac = types.InlineKeyboardMarkup()
    keyboard12cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard12cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cnore'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard12cac

# Функция ремонта
def cac_repair(chat_id):
    msg_del = state_storage.get_value(f'cac_caor_del:{chat_id}')
    try:
        bot.delete_message (chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\remont\\chern.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\remont\\need_rem.jpg', 'rb') as img2, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\remont\\cosmetic.jpg', 'rb') as img3, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\remont\\good.jpg', 'rb') as img4, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\remont\\design.jpg', 'rb') as img5:
        media = [InputMediaPhoto(img1, caption="Выберите тип ремонта из списка\n\n Черновая \n\n Нуждается в ремонте \n\n Только косметика \n\n Хороший \n\n Отличный \n\n Дизайнерский"),
            InputMediaPhoto(img2),
            InputMediaPhoto(img3),
            InputMediaPhoto(img4),
            InputMediaPhoto(img5)
            ]
        bot.send_media_group(chat_id, media)
    cr = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_cac13())
    state_storage.set_value(f'cac_cr_del:{chat_id}', cr.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')

def create_keyboard_cac13():
    keyboard13cac = types.InlineKeyboardMarkup()
    keyboard13cac.add(types.InlineKeyboardButton('Нуждается в серьёзном ремонте', callback_data='cac_price_big_repair'))
    keyboard13cac.add(types.InlineKeyboardButton('Черновая отделка', callback_data='cac_price_finishing'))
    keyboard13cac.add(types.InlineKeyboardButton('Нуждается в косметическом ремонте', callback_data='cac_price_cosmetic'))
    keyboard13cac.row(types.InlineKeyboardButton('Хороший ремонт', callback_data='cac_price_good'), types.InlineKeyboardButton('Отличный ремонт', callback_data='cac_price_perfect'))
    keyboard13cac.add(types.InlineKeyboardButton('Дизайнерский ремонт',  callback_data='cac_price_design'))
    keyboard13cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard13cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cta'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard13cac

# Создаём функцию ввода возраста ремонта
def cac_age_of_repair(chat_id):
    msgs_del = ['cac_cpf_del','cac_cr_del']
    for msg in msgs_del:
        try:
            mes_del = state_storage.get_value(f'{msg}:{chat_id}')
            try:
                bot.delete_message (chat_id, mes_del)
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except:
            pass
    update_state(chat_id, 'waiting_age_of_repair')
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\age_of_repair.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Введите возраст ремонта, в годах')
    caor = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard14cac())
    state_storage.set_value(f'cac_caor_del:{chat_id}', caor.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')
    
# Обработчик ввода возраста ремонта
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'waiting_age_of_repair')
def cac_age_of_repair_handler(message):
    chat_id = message.chat.id
    mes_del = state_storage.get_value(f'cac_caor_del:{chat_id}')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    message_age_repair = message.text
    try:
        age_repair = int(message_age_repair)
    except ValueError:
        bot.send_message(chat_id, 'Ошибка, не верный формат. Пожалуйста повторите ввод или свяжитесь со специалистом')
        cac_age_of_repair(chat_id)
    if age_repair < 0:
        bot.send_message(chat_id, 'Ошибка, число не должно быть отрицательным. Пожалуйста повторите ввод или свяжитесь со специалистом')
        cac_age_of_repair(chat_id)
    elif age_repair > 10:
        cac_repair_coef = 0.3
        bot.send_message(chat_id, f'Вы ввели {age_repair} года(лет).')
        cac_price_furniture(chat_id)
        user_id = chat_id
        state_storage.set_value(f'cac_repair_coef:{chat_id}', cac_repair_coef)
        cac_price_furniture(chat_id)
    else:
        cac_repair_coef = 0.01 + 0.03 * age_repair
        bot.send_message(chat_id, f'Вы ввели {age_repair} года(лет).')
        user_id = chat_id
        state_storage.set_value(f'cac_repair_coef:{chat_id}', cac_repair_coef)
        cac_price_furniture(chat_id)
        
def create_keyboard14cac():
    keyboard14cac = types.InlineKeyboardMarkup()
    keyboard14cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard14cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cr'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard14cac

# Функция ввода стоимости мебели и техники
def cac_price_furniture(chat_id):
    update_state(chat_id, 'waiting_price_of_furniture')
    with open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\furniture\\kitchen.jpg', 'rb') as img1, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\furniture\\bathroom.jpg', 'rb') as img2, \
        open('C:\\Users\\Admin\\Desktop\\bot_real_estate\\content\\calc_cac\\furniture\\tv.jpg', 'rb') as img3:
        media = [InputMediaPhoto(img1, caption="Введите стоимость мебели и техники, которую вы планируете оставить."),
            InputMediaPhoto(img2),
            InputMediaPhoto(img3)]
        bot.send_media_group(chat_id, media)
    bot.send_message(chat_id, 'Выберите один из вариантов')
    cpf = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard15cac())
    state_storage.set_value(f'cac_cpf_del:{chat_id}', cpf.message_id)
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_in_progress')

# Обработчик ввода стоимости мебели и техники
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'waiting_price_of_furniture')
def cac_price_furniture_handler(message):
    chat_id = message.chat.id
    mes_del = state_storage.get_value(f'cac_cpf_del:{chat_id}')
    try:
        bot.delete_message (chat_id, mes_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    user_id = chat_id
    message_furniture_cost = message.text
    try:
        furniture_price = int(message_furniture_cost)
    except ValueError:
        bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или свяжитесь со специалистом')
        cac_price_furniture(chat_id)
    if furniture_price < 0:
        bot.send_message(chat_id, 'Ошибка, число не должно быть отрицательным. Пожалуйста повторите ввод или свяжитесь со специалистом')
        cac_price_furniture(chat_id)
    else:
        state_storage.set_value(f'furniture_cost:{chat_id}', furniture_price)
        cac_repair_coef = state_storage.get_value(f'cac_repair_coef:{chat_id}')
        area = state_storage.get_value(f'area:{chat_id}')
        chosen_region_name = state_storage.get_value(f'chosen_region_name:{chat_id}')
        chosen_street_name = state_storage.get_value(f'chosen_street_name:{chat_id}')
        house_info1 = state_storage.get_value(f'house_info1:{chat_id}')
        house_info2 = state_storage.get_value(f'house_info2:{chat_id}')
        cac_age = state_storage.get_value(f'cac_age:{chat_id}')
        number_of_rooms = state_storage.get_value(f'number_of_rooms:{chat_id}')
        price_of_finishing = state_storage.get_value(f'price_of_finishing:{chat_id}')
        with Session() as session_furniture_cost:
            user = session_furniture_cost.query(CacUserData).filter_by(user_id=user_id).first()
            user.furniture_cost = furniture_price
            user.repair_coef = cac_repair_coef
            user.area = area
            user.chosen_region_name = chosen_region_name
            user.chosen_street_name = chosen_street_name
            user.house_info1 = house_info1
            user.house_info2 = house_info2        
            user.cac_age = cac_age
            user.number_of_rooms = number_of_rooms
            user.price_of_finishing = price_of_finishing
            session_furniture_cost.commit()
        cac_calculate_results(chat_id)

def create_keyboard15cac():
    keyboard15cac = types.InlineKeyboardMarkup()
    keyboard15cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard15cac.row(types.InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_caor'), types.InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return keyboard15cac

def cac_calculate_results(chat_id):
    msg_del = state_storage.get_value(f'cac_greet_del:{chat_id}')
    try:
        bot.delete_message(chat_id, msg_del)
    except Exception:
        pass
    state_storage.set_value(f'reminder_states:{chat_id}', 'cac_completed')
    msgs_del = ['cac_cpf_del', 'cac_greet_del']
    for msg in msgs_del:
        try:
            mes_del = state_storage.get_value(f'{msg}:{chat_id}')
            try:
                bot.delete_message (mes_del['chat_id'], mes_del['message_id'])
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except:
             pass
    # ПОЛЬЗОВАТЕЛЬСКИЕ ДАННЫЕ
    # Создаём кортежи с ценами постройки домов
    price_panel_brezh = (625, 675)
    price_panel_hruzh = (600, 650)
    price_panel_standart_project = (700, 725)
    price_panel_upgrade = (675, 700)
    price_brick_stalin = (750, 800)
    price_brick_hruzh = (650, 675)
    price_brick_brezh = (675, 700)
    price_brick_standart = (725, 750)
    price_brick_upgrade = (750, 775)
    price_monolith_brick = (750, 800)
    price_monolith_frame_and_block = (725, 775)
    price_monolith_panel = (700, 750)
    # Создаём списки, хранящие данные для работы с годом постройки и данные для рассчёта коэффициентов
    lifespan_panel = int(100)
    lifespan_brick = int(125)
    lifespan_monolith = int(150)
    cac_house_depr_coef = int(0)
    # Создаём списки для работы с кадастровой стоимостью
    kad_price_average_minsk = int(184)
    # ДАНННЫЕ О СТОИМОСТИ ОБЪЕКТОВ ПО ВИДУ ИХ РЕМОНТА
    # Черновая отделка
    price_finishing_m2 = (115, 130)
    # Нуждается в серьёзном ремонте
    price_big_repair_m2 = (90, 105)
    # Нуждается в косметическом ремонте
    price_cosmetic_m2 = (135, 150)
    # Хороший ремонт
    price_good_m2 = (175, 190)
    # Отличный ремонт
    price_perfect_m2 = (195, 210)
    # Евроремонт
    price_design_m2 = (265, 285)
    min_cac_flat_cost = 0
    max_cac_flat_cost = 0
    av_cac_flat_cost = 0
    user_id = chat_id
    try:
        with Session() as session_results2:
            user = session_results2.query(CacUserData).filter(CacUserData.user_id == user_id).one()
            chosen_region_name = user.chosen_region_name
            chosen_street_name = user.chosen_street_name
            house_info1 = user.house_info1
            house_info2 = user.house_info2
            number_of_rooms = user.number_of_rooms
            cac_age = user.cac_age
            area = user.area
            price_of_finishing = user.price_of_finishing
            repair_coef = user.repair_coef
            furniture_cost = user.furniture_cost
            session_results2.commit()
        user_data_check = True
    except Exception as e:
        user_data_check = False
    try:
    	# Район
        # ПОДКЛЮЧЕНИЕ К БД
        
        query_region_results2 = f"SELECT deals FROM regions{number_of_rooms} WHERE region_name = '{chosen_region_name}'"
        query_region_results2 = text(query_region_results2)
        with Session() as session_region_results2:
            result = session_region_results2.execute(query_region_results2)
        rows = result.fetchall()
        strings = [row[0] for row in rows]
        lists = [re.findall(r'\d+', string) for string in strings]
        lists = [[int(num) for num in lst] for lst in lists]
        comp_list1 = []
        for lst in lists:
          comp_list1.extend(lst)
        for value in comp_list1[:]:
            if value > 3500 or value < 600:
                comp_list1.remove(value)
        values = np.array(comp_list1)
        values.sort()
        mu = np.mean(values)
        sigma = np.std(values)
        weights = np.array([1 / (sigma * math.sqrt(2 * math.pi)) * math.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) for x in values])
        weighted_mean1 = np.average(values, weights=weights)
        weighted_sum = np.sum(weights * (values - weighted_mean1) ** 2)
        weighted_sum_weights = np.sum(weights)
        weighted_std_dev1 = math.sqrt(weighted_sum / weighted_sum_weights)
        comp_high1 = int(weighted_std_dev1 + weighted_mean1)
        comp_low1 = int(- weighted_std_dev1 + weighted_mean1)
        #Отрисовка графика
        data = values
        if number_of_rooms == 0:
          left_bound = np.quantile(data, 0.184)
          middle_bound = np.quantile(data, 0.348)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 1:
          left_bound = np.quantile(data, 0.34)
          middle_bound = np.quantile(data, 0.58)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 2:
          left_bound = np.quantile(data, 0.28)
          middle_bound = np.quantile(data, 0.47)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 3:
          left_bound = np.quantile(data, 0.37)
          middle_bound = np.quantile(data, 0.61)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 4:
          left_bound = np.quantile(data, 0.239)
          middle_bound = np.quantile(data, 0.49)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 5:
          left_bound = np.quantile(data, 0.22)
          middle_bound = np.quantile(data, 0.47)
          right_bound = np.quantile(data, 1)
        left = data[data < left_bound]
        middle = data[(left_bound <= data) & (data < middle_bound)]
        right = data[data >= middle_bound]
        fig, ax = plt.subplots()
        n, bins, patches = ax.hist(data, bins=100, edgecolor='black', color='white')
        colors_dict = {(-np.inf, left_bound): 'red',
                    (left_bound, middle_bound): '#DAB71A',
                    (middle_bound, right_bound): 'green'}
        alphas = [0.65, 0.6, 0.75]
        for i, patch in enumerate(patches):
            color = 'white'
            alpha = 1
            for j, ((low, high), c) in enumerate(colors_dict.items()):
                if low <= bins[i] < high:
                    color = c
                    alpha = alphas[j]
                    break
            patch.set_facecolor(color)
            patch.set_alpha(alpha)
        plt.xlabel('Цена м²')
        plt.ylabel('Количество проданных')
        if number_of_rooms == 0:
          plt.title(' Все районы, Доля')
        else:
          plt.title(f'{chosen_region_name}, {number_of_rooms} комн')
        colors = ['red', '#DAB71A', 'green']
        labels = ['Низкая рыночная стоимость', 'Средняя стоимость', 'Высокая рыночная стоимость']
        handles = [plt.Rectangle((0,0),1,1, color=c, alpha=a) for c, a in zip(colors, alphas)]
        plt.legend(handles, labels, loc='upper right')
        plt.savefig(f'C:\\Users/Admin/Desktop/bot_real_estate/bot/region_minsk_{chat_id}.jpg')
        q1, q3 = np.percentile(comp_list1, [25, 75])
        iqr1 = q3 - q1
        h1 = (2 * iqr1) / (len(comp_list1) ** (1/3))
        h1 = round(h1)
        interval_width1 = h1
        intervals1 = list(range(min(comp_list1), max(comp_list1) + interval_width1, interval_width1))
        counts1 = []
        for interval1 in intervals1:
            count1 = sum(1 for price in comp_list1 if interval1 <= price < interval1 + interval_width1)
            counts1.append(count1)
        comp_max_count1 = max(counts1)
        comp_max_index1 = counts1.index(comp_max_count1)
        comp_interval_mode1 = intervals1[comp_max_index1] + interval_width1 / 2
        comp_flat_max1 = int(comp_high1 * area)
        comp_flat_min1 = int(comp_low1 * area)
        comp_flat_av1 = int(comp_interval_mode1 * area)
    except Exception as e:
        comp_high1 = 0
        comp_low1 = 0
        comp_interval_mode1 = 0
    try:
        # УЛИЦА
        query_street_result2 = f"SELECT deals FROM streets{number_of_rooms} WHERE street_name = '{chosen_street_name}'"
        query_street_result2 = text(query_street_result2)
        with Session() as session_streets_result2:
            result = session_streets_result2.execute(query_street_result2)
        rows = result.fetchall()
        strings = [row[0] for row in rows]
        lists = [re.findall(r'\d+', string) for string in strings]
        lists = [[int(num) for num in lst] for lst in lists]
        comp_list2 = []
        for lst in lists:
          comp_list2.extend(lst)
        for value in comp_list2[:]:
            if value > 3500 or value < 600:
              comp_list2.remove(value)
        values = np.array(comp_list2)
        values.sort()
        mu = np.mean(values)
        sigma = np.std(values)
        weights = np.array([1 / (sigma * math.sqrt(2 * math.pi)) * math.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) for x in values])
        weighted_mean2 = np.average(values, weights=weights)
        weighted_sum = np.sum(weights * (values - weighted_mean2) ** 2)
        weighted_sum_weights = np.sum(weights)
        weighted_std_dev2 = math.sqrt(weighted_sum / weighted_sum_weights)
        comp_high2 = int(weighted_std_dev2 + weighted_mean2)
        comp_low2 = int(- weighted_std_dev2 + weighted_mean2)
        data = values
        if number_of_rooms == 0:
          left_bound = np.quantile(data, 0.184)
          middle_bound = np.quantile(data, 0.348)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 1:
          left_bound = np.quantile(data, 0.34)
          middle_bound = np.quantile(data, 0.58)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 2:
          left_bound = np.quantile(data, 0.28)
          middle_bound = np.quantile(data, 0.47)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 3:
          left_bound = np.quantile(data, 0.37)
          middle_bound = np.quantile(data, 0.61)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 4:
          left_bound = np.quantile(data, 0.239)
          middle_bound = np.quantile(data, 0.49)
          right_bound = np.quantile(data, 1)
        elif number_of_rooms == 5:
          left_bound = np.quantile(data, 0.22)
          middle_bound = np.quantile(data, 0.47)
          right_bound = np.quantile(data, 1)
        left = data[data < left_bound]
        middle = data[(left_bound <= data) & (data < middle_bound)]
        right = data[data >= middle_bound]
        fig, ax = plt.subplots()
        n, bins, patches = ax.hist(data, bins=100, edgecolor='black', color='white')
        colors_dict = {(-np.inf, left_bound): 'red',
                    (left_bound, middle_bound): '#DAB71A',
                    (middle_bound, right_bound): 'green'}
        alphas = [0.65, 0.6, 0.75]
        for i, patch in enumerate(patches):
            color = 'white'
            alpha = 1
            for j, ((low, high), c) in enumerate(colors_dict.items()):
                if low <= bins[i] < high:
                    color = c
                    alpha = alphas[j]
                    break
            patch.set_facecolor(color)
            patch.set_alpha(alpha)
        plt.xlabel('Цена м²')
        plt.ylabel('Количество проданных')
        if number_of_rooms == 0:
          plt.title(f'{chosen_street_name}, Доля')
        else:
          plt.title(f'{chosen_street_name}, {number_of_rooms} комн')
        colors = ['red', '#DAB71A', 'green']
        labels = ['Низкая рыночная стоимость', 'Средняя стоимость', 'Высокая рыночная стоимость']
        handles = [plt.Rectangle((0,0),1,1, color=c, alpha=a) for c, a in zip(colors, alphas)]
        plt.legend(handles, labels, loc='upper right')
        plt.savefig(f'C:/Users/Admin/Desktop/bot_real_estate/bot/street_{chat_id}.jpg')
        q1, q3 = np.percentile(comp_list1, [25, 75])
        iqr2 = q3 - q1
        h2 = (2 * iqr2) / (len(comp_list2) ** (1/3))
        h2 = round(h2)
        interval_width2 = h2
        intervals2 = list(range(min(comp_list2), max(comp_list2) + interval_width2, interval_width2))
        counts2 = []
        for interval2 in intervals2:
            count2 = sum(1 for price in comp_list2 if interval2 <= price < interval2 + interval_width2)
            counts2.append(count2)
        comp_max_count2 = max(counts2)
        comp_max_index2 = counts2.index(comp_max_count2)
        comp_interval_mode2 = intervals2[comp_max_index2] + interval_width2 / 2
        comp_flat_max2 = int(comp_high2 * area)
        comp_flat_min2 = int(comp_low2 * area)
        comp_flat_av2 = int(comp_interval_mode2 * area)
    except Exception as e:
        comp_low2 = 0
        comp_high2 = 0
        comp_interval_mode2 =0
        comp_flat_max2 = 0
        comp_flat_min2 = 0
        comp_flat_av2 =0
    try:
        if house_info1 == "panel" and house_info2 == "hrush":
          cost_min_house_price = int(price_panel_hruzh[0])
          cost_max_house_price = int(price_panel_hruzh[1])
        elif house_info1 == "panel" and house_info2 == "brezh":
          cost_min_house_price = int(price_panel_brezh[0])
          cost_max_house_price = int(price_panel_brezh[1])
        elif house_info1 == "panel" and house_info2 == "standart":
          cost_min_house_price = int(price_panel_standart_project[0])
          cost_max_house_price = int(price_panel_standart_project[1])
        elif house_info1 == "panel" and house_info2 == "upgrade":
          cost_min_house_price = int(price_panel_upgrade[0])
          cost_max_house_price = int(price_panel_upgrade[1])
        elif house_info1 == "brick" and house_info2 == "stalin":
          cost_min_house_price = int(price_brick_stalin[0])
          cost_max_house_price = int(price_brick_stalin[1])
        elif house_info1 == "brick" and house_info2 == "hrush":
          cost_min_house_price = int(price_brick_hruzh[0])
          cost_max_house_price = int(price_brick_hruzh[1])
        elif house_info1 == "brick" and house_info2 == "brezh":
          cost_min_house_price = int(price_brick_brezh[0])
          cost_max_house_price = int(price_brick_brezh[1])
        elif house_info1 == "brick" and house_info2 == "standart":
          cost_min_house_price = int(price_brick_standart[0])
          cost_max_house_price = int(price_brick_standart[1])
        elif house_info1 == "brick" and house_info2 == "upgrade":
          cost_min_house_price = int(price_brick_upgrade[0])
          cost_max_house_price = int(price_brick_upgrade[1])
        elif house_info1 == "monolith" and house_info2 == "mon_brick":
          cost_min_house_price = int(price_monolith_brick[0])
          cost_max_house_price = int(price_monolith_brick[1])
        elif house_info1 == "monolith" and house_info2 == "mon_panel":
          cost_min_house_price = int(price_monolith_panel[0])
          cost_max_house_price = int(price_monolith_panel[1])
        elif house_info1 == "monolith" and house_info2 == "mon_block":
          cost_min_house_price = int(price_monolith_frame_and_block[0])
          cost_max_house_price = int(price_monolith_frame_and_block[1])
        if house_info1 == "panel":
          cost_house_depr_coef = cac_age / lifespan_panel
          if cost_house_depr_coef > 0.4:
            cost_house_depr_coef = 0.4
        elif house_info1 == "brick":
          cost_house_depr_coef = cac_age / lifespan_brick
          if cost_house_depr_coef > 0.4:
            cost_house_depr_coef = 0.4
        elif house_info1 == "monolith":
          cost_house_depr_coef = cac_age / lifespan_monolith
          if cost_house_depr_coef > 0.4:
            cost_house_depr_coef = 0.4
        if price_of_finishing == "price_finishing":
          min_cost_price_of_finishing = int(price_finishing_m2[0])
          max_cost_price_of_finishing = int(price_finishing_m2[1])
        elif price_of_finishing == "price_big_repair":
          min_cost_price_of_finishing = int(price_big_repair_m2[0])
          max_cost_price_of_finishing = int(price_big_repair_m2[1])
        elif price_of_finishing == "price_cosmetic":
          min_cost_price_of_finishing = int(price_cosmetic_m2[0])
          max_cost_price_of_finishing = int(price_cosmetic_m2[1])
        elif price_of_finishing == "price_good":
          min_cost_price_of_finishing = int(price_good_m2[0])
          max_cost_price_of_finishing = int(price_good_m2[1])
        elif price_of_finishing == "price_perfect":
          min_cost_price_of_finishing = int(price_perfect_m2[0])
          max_cost_price_of_finishing = int(price_perfect_m2[1])
        elif price_of_finishing == "price_design":
          min_cost_price_of_finishing = int(price_design_m2[0])
          max_cost_price_of_finishing = int(price_design_m2[1])
        if chosen_region_name == "Центральный район":
          cost_cad_price = kad_price_average_minsk * (343 / 234)
        elif chosen_region_name == "Фрунзенский район":
          cost_cad_price = kad_price_average_minsk * (273 / 234)
        elif chosen_region_name == "Советский район":
          cost_cad_price = kad_price_average_minsk * (283 / 234)
        elif chosen_region_name == "Первомайский район":
          cost_cad_price = kad_price_average_minsk * (253 / 234)
        elif chosen_region_name == "Партизанский район":
          cost_cad_price = kad_price_average_minsk * (238 / 234)
        elif chosen_region_name == "Заводской район":
          cost_cad_price = kad_price_average_minsk
        elif chosen_region_name == "Ленинский район":
          cost_cad_price = kad_price_average_minsk * (254 / 234)
        elif chosen_region_name == "Октябрьский район":
          cost_cad_price = kad_price_average_minsk * (257 / 234)
        elif chosen_region_name == "Московский район":
          cost_cad_price = kad_price_average_minsk * (265 / 234)
        min_flat_cost_price = int(((cost_min_house_price - (cost_min_house_price * cost_house_depr_coef)) + (min_cost_price_of_finishing - (min_cost_price_of_finishing * repair_coef)) + cost_cad_price) * area + furniture_cost)
        max_flat_cost_price = int(((cost_max_house_price - (cost_max_house_price * cost_house_depr_coef)) + (max_cost_price_of_finishing - (max_cost_price_of_finishing * repair_coef)) + cost_cad_price) * area + furniture_cost)
        av_flat_cost_price = int((max_flat_cost_price + min_flat_cost_price) / 2)        
    except Exception as e:
        min_flat_cost_price = 0
        av_flat_cost_price = 0
        max_flat_cost_price = 0
       # Финальный рассчёт 
    try:
        if user_data_check == False:
            # Ошибка
            bot.send_message(chat_id, '😱Опаньки, похоже возникли проблемы.😱\n Если вы не пользовались функцией рассчёта раньше, то нужно ей воспользоваться, \n я не могу взять данные вашей о вашем объекте из воздуха. \n Пожалуйста, воспользуйтесь функцией рассчёта, \n с помощью кнопки начать. 😁')
            send_greeting_cac(chat_id)
        elif comp_high1 == 0 and comp_low1 == 0 and comp_interval_mode1 == 0:
            bot.send_message(chat_id, f'Ошибка, нет данных о сделках по {chosen_region_name}. \n На сервере проводятся работы, повторите запрос позже.')
            send_greeting_cac(chat_id)
        elif comp_low2 == 0 and comp_high2 == 0 and comp_interval_mode2 == 0:
            # Затратный
            bot.send_message(chat_id, f'** ЗАТРАТНЫЙ АНАЛИЗ СТОИМОСТИ ОБЪЕКТА ** \n\n Исходя из введённых вами данных, был произведён рассчёт стоимости вашего объекта. \n Рекомендуемый диапозон для продажи, без учёта данных сделок: {min_flat_cost_price} — {max_flat_cost_price}', parse_mode='markdown')
            # Сравнительный район
            with open(f'C:/Users/Admin/Desktop/bot_real_estate/bot/region_minsk_{chat_id}.jpg', 'rb') as img_region:
              bot.send_photo(chat_id, img_region, caption=f'** СРАВНИТЕЛЬНЫЙ АНАЛИЗ \n ДАННЫЕ СДЕЛОК, {chosen_region_name.upper()} **\n\n Цена, которая чаще всего встречается в выбранном районе($/м2): {comp_interval_mode1} \n Минимальная зафиксированная цена, в выбранном районе($/м2): {min(values)} \n Максимальная зафиксированная цена, в выбранном районе($/м2): {max(values)} \n Рекомендуемый ценовой диапозон, без учёта данных сделок на вашей улице(общий прогноз): {int(comp_low1 * area)} — {int(comp_high1 * area)}', parse_mode='markdown')
            os.remove(f'C:/Users/Admin/Desktop/bot_real_estate/bot/region_minsk_{chat_id}.jpg')              
            bot.send_message(chat_id, f"Ошибка, нет сделок на ул. {chosen_street_name} по заданным параметрам. \n Внимание, точность рассчёта снижена, рекомендуем проконсультироваться со специалистом.")
            min_cac_flat_cost = int((min_flat_cost_price + (comp_flat_min1 * 5)) / 6)
            max_cac_flat_cost = int((max_flat_cost_price + (comp_flat_max1 * 7)) / 8)
            av_cac_flat_cost = int((av_flat_cost_price + (comp_flat_av1 * 5)) / 6)
            cac_all = [min_cac_flat_cost, max_cac_flat_cost, av_cac_flat_cost, min_flat_cost_price, comp_flat_min1, max_flat_cost_price, comp_flat_max1, av_flat_cost_price, comp_flat_av1]
            cac_all_dev = statistics.stdev(cac_all)
            cac_all_max_price = av_cac_flat_cost + cac_all_dev
            cac_all_min_price = av_cac_flat_cost - cac_all_dev
            bot.send_message(chat_id, f'** ИТОГОВЫЙ АНАЛИЗ СТОИМОСТИ ОБЪЕКТА ** \n\n Исходя из всех вышеперечисленных анализов и введённых вами данных, был произведён рассчет максимально приемлемого диапазона, для продажи. \n Рекомендуемый ценовой диапазон для продажи вашего объекта: {cac_all_min_price} — {cac_all_max_price}\nВНИМАНИЕ!!! Стоимость может изменяться из-за смены рыночной коньюктуры(как в вашу пользу, так и против вас)', parse_mode='Markdown')
            msg1489 = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_cac17())
            state_storage.set_value(f'cac_ccr_del:{chat_id}', msg1489.message_id)
        else:
            # Затратный
            bot.send_message(chat_id, f'** ЗАТРАТНЫЙ АНАЛИЗ СТОИМОСТИ ОБЪЕКТА ** \n\n Исходя из введённых вами данных, был произведён рассчёт стоимости вашего объекта. \n Рекомендуемый диапозон для продажи, без учёта данных сделок: {min_flat_cost_price} — {max_flat_cost_price}', parse_mode='markdown')
            # Сравнительный район
            with open(f'C:/Users/Admin/Desktop/bot_real_estate/bot/region_minsk_{chat_id}.jpg', 'rb') as img_region:
              bot.send_photo(chat_id, img_region, caption=f'** СРАВНИТЕЛЬНЫЙ АНАЛИЗ \n ДАННЫЕ СДЕЛОК, {chosen_region_name.upper()} **\n\n Цена, которая чаще всего встречается в выбранном районе($/м2): {comp_interval_mode1} \n Минимальная зафиксированная цена, в выбранном районе($/м2): {min(values)} \n Максимальная зафиксированная цена, в выбранном районе($/м2): {max(values)} \n Рекомендуемый ценовой диапозон, без учёта данных сделок на вашей улице(общий прогноз): {int(comp_low1 * area)} — {int(comp_high1 * area)}', parse_mode='markdown')
            os.remove(f'C:/Users/Admin/Desktop/bot_real_estate/bot/region_minsk_{chat_id}.jpg')              
            # Сравнительный улица
            with open(f'C:/Users/Admin/Desktop/bot_real_estate/bot/street_{chat_id}.jpg', 'rb') as img_street:
              bot.send_photo(chat_id, img_street, caption=f'** СРАВНИТЕЛЬНЫЙ АНАЛИЗ \n ДАННЫЕ СДЕЛОК, {chosen_street_name.upper()}**\n\n Цена, которая чаще всего встречается на выбранной улице($/м2): {comp_interval_mode2} \n Минимальная зафиксированная цена, на выбранной улице($/м2): {min(values)} \n Максимальная зафиксированная цена, на выбранной улице($/м2): {max(values)} \n Рекомендуемый ценовой диапозон, без учёта данных сделок района и ремонта(относительный прогноз): {int(comp_low2 * area)} — {int(comp_high2 * area)}', parse_mode='Markdown')
            os.remove(f'C:/Users/Admin/Desktop/bot_real_estate/bot/street_{chat_id}.jpg')
            min_cac_flat_cost = int((min_flat_cost_price + comp_flat_min2 + (comp_flat_min1 * 5)) / 7)
            max_cac_flat_cost = int((max_flat_cost_price + comp_flat_max2 + (comp_flat_max1 * 7)) / 9)
            av_cac_flat_cost = int((av_flat_cost_price + comp_flat_av2 + (comp_flat_av1 * 5)) / 7) 
            cac_all = [min_cac_flat_cost, max_cac_flat_cost, av_cac_flat_cost, min_flat_cost_price, comp_flat_min2, comp_flat_min1, max_flat_cost_price, comp_flat_max2, comp_flat_max1, av_flat_cost_price, comp_flat_av2, comp_flat_av1]
            cac_all_dev = statistics.stdev(cac_all)
            cac_all_max_price = av_cac_flat_cost + cac_all_dev
            cac_all_min_price = av_cac_flat_cost - cac_all_dev
            bot.send_message(chat_id, f'** ИТОГОВЫЙ АНАЛИЗ СТОИМОСТИ ОБЪЕКТА **  \n\n Исходя из всех вышеперечисленных анализов и введённых вами был произведён рассчет максимально приемлемого диапазона, для продажи вашего объекта: \n Точка эквилибриума: {int(av_cac_flat_cost)} \n Рекомендуемый ценовой диапазон для продажи вашего объекта: {int(cac_all_min_price)} — {int(cac_all_max_price)}\n **ВНИМАНИЕ!!!** Стоимость может изменяться из-за смены рыночной коньюктуры(как в вашу пользу, так и против вас)', parse_mode='Markdown')
            msg1488 = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_cac17())
            state_storage.set_value(f'cac_ccr_del:{chat_id}', msg1488.message_id)
    except Exception as e:
        # Ошибка
        bot.send_message(chat_id, '😱 Опаньки, похоже возникли проблемы.😱\n Если вы не пользовались функцией рассчёта раньше, то нужно ей воспользоваться, \n я не могу взять данные вашей о вашем объекте из воздуха. \n Пожалуйста, воспользуйтесь функцией рассчёта, \n с помощью кнопки начать. 😁')
        send_greeting_cac(chat_id)

def create_keyboard_cac17():
    keyboard17cac = types.InlineKeyboardMarkup()
    keyboard17cac.row(types.InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
    keyboard17cac.add(types.InlineKeyboardButton('Главное меню', callback_data='menu'))
    return keyboard17cac

# РЕСТАРТ
def cac_func_restart(chat_id):
    msgs_del =['cac_region_choice_del', 'cac_fin_street_choice_del', 'cac_chn_del',
               'cac_ctoh_del', 'cac_ctm_del', 'cac_ctp_del',
               'cac_ctb_del', 'cac_caoh_del', 'cac_cnore_del',
               'cac_cta_del', 'cac_cpf_del', 'cac_ccr_del']
    for mes_del in msgs_del:
        try:
            msg = state_storage.get_value(f'{mes_del}:{chat_id}')
            try:
                bot.delete_message (chat_id, msg)
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except Exception as e:
            pass
        











# AI функционал
def chat_bot(chat_id):
    update_state(chat_id, 'kuzia_chatbot')
    msgs_del = ['main_del', 'ai_del']
    for mes_del in msgs_del:
        try:
            msg = state_storage.get_value(f'{mes_del}:{chat_id}')
            try:
                bot.delete_message(chat_id, msg)
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except:
            pass
    with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/hello.jpg','rb') as img1:
        bot.send_photo(chat_id, img1, caption='Напишите свой вопрос и отправьте мне, а я постараюсь найти на него ответ.\n Это может занять некоторое время, потому что это не так просто как кажется.\n Спасибо.')
    message = bot.send_message(chat_id, 'Меню', reply_markup=create_chat_keyboard1())
    state_storage.set_value(f'ai_del:{chat_id}', message.message_id)

@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'kuzia_chatbot')
def chat_bot_result(message):
    chat_id = message.chat.id
    msg_del = state_storage.get_value(f'ai_del:{chat_id}')
    update_state(chat_id, 'kuzia_chatbot_inf')
    try:
        bot.delete_message(chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    question = message.text
    try:
        client = Client()
        response = client.chat.completions.create(
        model="gpt-4-turbo",
        provider = g4f.Provider.Bing,
        messages=[{"role": "user", "content": f"Тебя зовут Кузя. Ты помошник агенства недвижимости Дом и Точка. Ты работаешь на территории РБ, просто помни. Ты отвечаешь на вопрос '{question}'"}]
        )
        answer = response.choices[0].message.content
        bot.send_message(chat_id, f'{answer}', parse_mode='Markdown')
    except Exception as e:
        pass
        bot.send_message(chat_id, 'Занят, не могу говорить, можете пообщаться со специалистом.\n Попробуйте повторить запрос позже.')
    message = bot.send_message(chat_id, 'Меню', reply_markup=create_chat_keyboard1())
    state_storage.set_value(f'ai_del:{chat_id}', message.message_id)

@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'kuzia_chatbot_inf')
def chat_bot_inf_result(message):
    chat_id = message.chat.id
    msg_del = state_storage.get_value(f'ai_del:{chat_id}')
    update_state(chat_id, 'kuzia_chatbot_inf')
    try:
        bot.delete_message(chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    update_state(chat_id, 'kuzia_chatbot')
    question = message.text
    try:
        client = Client()
        response = client.chat.completions.create(
        model="gpt-4-turbo",
        provider = g4f.Provider.Bing,
        messages=[{"role": "user", "content": f"Тебя зовут Кузя. Ты помошник агенства недвижимости Дом и Точка. Ты работаешь на территории РБ, просто помни. Ты отвечаешь на вопрос '{question}'"}]
        )
        answer = response.choices[0].message.content
        bot.send_message(chat_id, f'{answer}', parse_mode='Markdown')
    except Exception as e:
        bot.send_message(chat_id, 'Занят, не могу говорить, можете пообщаться со специалистом.\n Попробуйте повторить запрос позже.')
    message = bot.send_message(chat_id, 'Меню', reply_markup=create_chat_keyboard1())
    state_storage.set_value(f'ai_del:{chat_id}', message.message_id)

def create_chat_keyboard1():
    chat_keyboard1 = types.InlineKeyboardMarkup()
    chat_keyboard1.row(types.InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), types.InlineKeyboardButton('Наш сайт', url='https://domitochka.pro'))
    chat_keyboard1.add(types.InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
    return chat_keyboard1
    
def services(chat_id):
    msgs_del = ['main_del']
    for msg_del in msgs_del:
        try:
            mes_del = state_storage.get_value(f'{msg_del}:{chat_id}')
            try:
                bot.delete_message (chat_id, mes_del)
            except telebot.apihelper.ApiTelegramException as e:
                pass
        except:
            pass
    with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/services/services.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Полное описание услуг', parse_mode='markdown')
        msg = bot.send_message(chat_id, 'Меню', reply_markup=create_services_keyboard())
    state_storage.set_value(f'services_del:{chat_id}', msg.message_id)

def create_services_keyboard():
    keyboard1services = types.InlineKeyboardMarkup()
    keyboard1services.add(types.InlineKeyboardButton('Продажа недвижимости под ключ', callback_data='services_sell'))
    keyboard1services.add(types.InlineKeyboardButton('Поиск дома мечты', callback_data='services_buy'))
    keyboard1services.add(types.InlineKeyboardButton('Помощь в оформлении документов и регистрации', callback_data='services_docs'))
    keyboard1services.add(types.InlineKeyboardButton('Главное меню', callback_data='menu'))
    return keyboard1services
   
def services_sell(chat_id):
    #update_state(chat_id, 'waiting_contact_data_sell')
    msg_del = state_storage.get_value(f'services_del:{chat_id}')
    try:
        bot.delete_message(chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    type_of_service = state_storage.get_value(f'type_of_service:{chat_id}')
    if type_of_service == 'sell':
        with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/services/services.jpg', 'rb') as img1:
            bot.send_photo(chat_id, img1)
        bot.send_message(chat_id, 'Описание продажи', reply_markup=create_keyboard_services_sell1())
    elif type_of_service == 'buy':
        with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/services/services.jpg', 'rb') as img1:
            bot.send_photo(chat_id, img1)
        bot.send_message(chat_id, 'Описание покупки', reply_markup=create_keyboard_services_sell1())
    elif type_of_service == 'docs':
        with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/services/services.jpg', 'rb') as img1:
            bot.send_photo(chat_id, img1)
        bot.send_message(chat_id, 'Описание документов', reply_markup=create_keyboard_services_sell1())
    msg = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_services_sell2(chat_id))
    state_storage.set_value(f'services_sell_del:{chat_id}', msg.message_id)

def create_keyboard_services_sell1():
    keyboard_services_sell1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard_services_sell1.add(types.KeyboardButton('Оставить заявку', request_contact=True))
    return keyboard_services_sell1

def create_keyboard_services_sell2(chat_id):
    type_of_service = state_storage.get_value(f'type_of_service:{chat_id}')
    keyboard_services_sell2 = types.InlineKeyboardMarkup()
    keyboard_services_sell2.add(types.InlineKeyboardButton('Написать в телеграмм', url='https://t.me/domitochka5'))
    if type_of_service == 'sell':
        keyboard_services_sell2.add(types.InlineKeyboardButton('Как это работает ?', url='https://domitochka.pro/prodazhanedvizhimoztipodkluzh'))
    elif type_of_service == 'buy':
        keyboard_services_sell2.add(types.InlineKeyboardButton('Как это работает ?', url='https://domitochka.pro/poiskdomamechti'))
    elif type_of_service == 'docs':
        keyboard_services_sell2.add(types.InlineKeyboardButton('Как это работает ?', url='https://domitochka.pro/documents'))
    keyboard_services_sell2.add(types.InlineKeyboardButton('Главное меню', callback_data='menu'))
    return keyboard_services_sell2

#@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'waiting_contact_data_sell')
@bot.message_handler(content_types=['contact'])
def services_sell_handler(message):
    chat_id = message.from_user.id
    update_state(chat_id, 'waiting_question_services')
    msg_del = state_storage.get_value(f'services_sell_del:{chat_id}')
    try:
        bot.delete_message(chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    if message.contact is not None:
        try:
            user_link = f"https://t.me/{message.from_user.username}"
            name = message.contact.first_name
            surname = message.contact.last_name
            phone = message.contact.phone_number
            state_storage.set_value(f'name:{chat_id}', name)
            state_storage.set_value(f'surname:{chat_id}', surname)
            state_storage.set_value(f'phone:{chat_id}', phone)
            state_storage.set_value(f'user_link:{chat_id}', user_link)
            try:
                bot.delete_message(chat_id, message.message_id)
            except telebot.apihelper.ApiTelegramException as e:
                print(e)
        except:
            pass
    else:
        pass
    with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/services/services.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='У вас есть какие-нибудь дополнительные вопросы ?', reply_markup=types.ReplyKeyboardRemove())
    msg = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_sevices_sell3(chat_id))
    state_storage.set_value(f'serv_sell_handler_del:{chat_id}', msg.message_id)
    return (user_link, name, surname, phone)

@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'waiting_question_services')
def services_sell_final1(message):
    chat_id = message.chat.id
    name = state_storage.get_value(f'name:{chat_id}')
    surname = state_storage.get_value(f'surname:{chat_id}')
    user_link = state_storage.get_value(f'user_link:{chat_id}')
    phone = state_storage.get_value(f'phone:{chat_id}')
    type_of_service = state_storage.get_value(f'type_of_service:{chat_id}')
    msg_del = state_storage.get_value(f'services_sell_del:{chat_id}')
    try:
        bot.delete_message(chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/services/services.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Спасибо')
    question = message.text
    if type_of_service == 'sell':
        type_of_service_msg = 'Продажа недвижимости'
    elif type_of_service == 'buy':
        type_of_service_msg = 'Покупка или побор недвижимости'
    elif type_of_service == 'docs':
        type_of_service_msg = 'Помощь в оформлении документов'
    email_sender = EmailSender()
    form = f'Дата заявки: {datetime.datetime.now()}\n Номер телефона:{phone}\n Тип услуги: {type_of_service_msg}\n Как подписан в тг:{name} {surname}\n Ссылка на профиль: {user_link}\n Вопрос: {question}'
    email_sender.send_email('Лид', form, 'domitochka@bk.ru')
    email_sender.send_email('Лид', form, 'pavelkutia@gmail.com')
    admins = [os.getenv('ADMIN1'), os.getenv('ADMIN2')]
    for admin_id in admins:
        bot.send_message(admin_id, form)
    msg = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_service_final())    
    state_storage.set_value(f'services_final_del:{chat_id}', msg.message_id)

def services_sell_final2(chat_id):
    name = state_storage.get_value(f'name:{chat_id}')
    surname = state_storage.get_value(f'surname:{chat_id}')
    user_link = state_storage.get_value(f'user_link:{chat_id}')
    phone = state_storage.get_value(f'phone:{chat_id}')
    type_of_service = state_storage.get_value(f'type_of_service:{chat_id}')
    msg_del = state_storage.get_value(f'services_sell_dell:{chat_id}')
    try:
        bot.delete_message(chat_id, msg_del)
    except telebot.apihelper.ApiTelegramException as e:
        pass
    with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/services/services.jpg', 'rb') as img1:
        bot.send_photo(chat_id, img1, caption='Спасибо')
    if type_of_service == 'sell':
        type_of_service_msg = 'Продажа недвижимости'
    elif type_of_service == 'buy':
        type_of_service_msg = 'Покупка или побор недвижимости'
    elif type_of_service == 'docs':
        type_of_service_msg = 'Помощь в оформлении документов'
    email_sender = EmailSender()
    form = f'Дата заявки: {datetime.datetime.now()}\n Номер телефона:{phone}\n Тип услуги: {type_of_service_msg}\n Как подписан в тг:{name} {surname}\n Ссылка на профиль: {user_link}\n Вопрос: без вопроса'
    email_sender.send_email('Лид', form, 'domitochka@bk.ru')
    email_sender.send_email('Лид', form, 'pavelkutia@gmail.com')
    admins = [os.getenv('ADMIN1'), os.getenv('ADMIN2')]
    for admin_id in admins:
        bot.send_message(admin_id, form)
    msg = bot.send_message(chat_id, 'Меню', reply_markup=create_keyboard_service_final())    
    state_storage.set_value(f'services_final_del:{chat_id}', msg.message_id)
 
def create_keyboard_service_final():
    keyboard_service_final = types.InlineKeyboardMarkup()
    keyboard_service_final.add(types.InlineKeyboardButton('Главное меню', callback_data='menu'))
    return keyboard_service_final

def create_keyboard_sevices_sell3(chat_id):
    keyboard_services_sell3 = types.InlineKeyboardMarkup()
    keyboard_services_sell3.add(types.InlineKeyboardButton('Вопросов нет, отправить заявку', callback_data='services_sell_final'))
    keyboard_services_sell3.add(types.InlineKeyboardButton('Главное меню', callback_data='menu'))
    return keyboard_services_sell3


# ОБРАБОТЧИК КЛАВИАТУРЫ






def send_message_to_all():
    now = datetime.datetime.now()
    if 18 <= now.hour <= 21:
        try:
            with Session() as session_mail_send:
                users = session_mail_send.query(User).all()
                for user in users:
                    if user.active:
                        user.messages += 1
                        if user.messages == 1:
                            url='https://vc.ru/u/1529738-pashtet-medved/806795-kak-prodat-kvartiru-za-rekordnuyu-cenu-ispolzuem-dizayn-socseti-i-kontent'
                            with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/mail/1.jpg', 'rb') as img1:
                                bot.send_photo(user.uid, img1, caption=f'Добрый вечер, {user.nick1} {user.nick2}!\n Мы подготовили статью о том насколько важна широкая, а главное грамотная рекламная кампания при продаже недвижимости.\n С ней вы можете ознакомится по ссылке ниже', reply_markup=create_keyboard_mail1(url))
                        elif user.messages == 2:
                            url='https://vc.ru/u/1529738-pashtet-medved/803809-dohodnyy-analiz-ceny-kak-prodat-po-maksimumu-kommercheskuyu-nedvizhimost-i-zhile-pod-arendu'
                            with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/mail/2.jpg', 'rb') as img1:
                                bot.send_photo(user.uid, img1, caption=f'{user.nick1} {user.nick2}, добрый вечер. У меня снова для вас порция развивающий информации, на этот раз мы затронем оценку недвижимости \n доходным способом, он позволяет не только рассчитать стоимость, но и вычислить \n прибыльность сдачи недвижимости в аренду. Ссылка ниже ...', reply_markup=create_keyboard_mail1(url))
                        elif user.messages == 3:
                            url='https://vc.ru/u/1529738-pashtet-medved/812682-kak-provesti-analiz-rynka-nedvizhimosti-poshagovoe-rukovodstvo-dlya-investorov-pokupateley-i-prodavcov'
                            with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/mail/3.jpg', 'rb') as img1:
                                bot.send_photo(user.uid, img1, caption=f'И снова здравствуйте, {user.nick1} {user.nick2}! \n Не хотите взглянуть на материал о том как научится оценивать перспективы на рынке недвижимости? \n Если горите желанием, ссылочка будет ниже.', reply_markup=create_keyboard_mail1(url))
                        elif user.messages == 4:
                            url='https://vc.ru/u/1529738-pashtet-medved/883502-dohodnyy-sposob-ocenki-nedvizhimosti-s-ispolzovaniem-zakona-metkalfa'
                            with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/mail/4.jpg', 'rb') as img1:
                                bot.send_photo(user.uid, img1, caption=f'Как вам вечер, {user.nick1} {user.nick2}?\n Не хотите скоратать его за прочтением чего-то интересного?\n Там у нас есть замечательный материал о нестандартном методе оценки, если что ссылка как всегда ниже...', reply_markup=create_keyboard_mail1(url))
                        elif user.messages == 5:
                            url='https://vc.ru/u/1529738-pashtet-medved/801207-zatratnyy-metod-ocenki-nedvizhimosti-kak-uznat-cenu-nizhe-kotoroy-prodavat-nelzya'
                            with open('C:/Users/Admin/Desktop/bot_real_estate/bot/content/mail/5.jpg', 'rb') as img1:
                                bot.send_photo(user.uid, img1, caption=f'Я вам не помешал, {user.nick1} {user.nick2}? У меня для вас шикарное предложение, не хотите скоротать полчасика \n за прочтением хорошего материала о том как оценить недвижимость по её характеристикам. И да ссылочка снизу.', reply_markup=create_keyboard_mail1(url))
        except telebot.apihelper.ApiTelegramException as e:
            pass
def create_keyboard_mail1(url):
    mail_keyboard1 = types.InlineKeyboardMarkup()
    mail_keyboard1.add(types.InlineKeyboardButton('Открыть статью', url=url))
    return mail_keyboard1

def send_reminders():
    reminder_states = state_storage.get_all_reminder_states()
    for chat_id, state in reminder_states.items():
        try:
            if state == 'cac_started':
                message = 'Похоже, вы забыли обо мне😥! Чем я могу помочь сегодня?'
            elif state == 'cac_in_progress':
                message = 'Я заметил, что вы не завершили ваш запрос. Есть что-то, в чем я могу помочь?'
            elif state == 'r_in_started':
                message = 'Похоже, вы забыли обо мне😥! Чем я могу помочь сегодня?'
            elif state == 'r_in_progress':
                message = 'Я заметил, что вы не завершили ваш запрос. Есть что-то, в чем я могу помочь?'
            bot.send_message(chat_id, message)
        except Exception as e:
            pass

def schedule_message_sending():
    hour = random.randint(18, 20)
    minute = random.randint(0, 59)
    time_str = f"{hour:02d}:{minute:02d}"
    schedule.every(2).days.at(time_str).do(send_message_to_all)

schedule_message_sending()

def reschedule_message_sending():
    schedule.clear(send_message_to_all)
    schedule_message_sending()

schedule.every(2).days.at("21:01").do(reschedule_message_sending)
schedule.every(3).hours.do(send_reminders)
schedule.every(2).days.at("18:00").do(send_message_to_all)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

def main():
    bot.infinity_polling(none_stop=True)

if __name__ == '__main__':
    main()


	
