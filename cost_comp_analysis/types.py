from abc import ABC
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class CostComparativeAnalysisMarkups(ABC):
    def __init__(self) -> None:
        super().__init__()


    def create_keyboard1(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('🔍 Пожалуй начнём', callback_data='cac_minsk_region_entry'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        keyboard.add(InlineKeyboardButton('💼 Расчёт по сохранёным параметрам', callback_data='cac_calculate_results'))
        keyboard.add(InlineKeyboardButton('Как это работает ?¿?', url='https://vc.ru/u/1529738-pashtet-medved/800356-sravnitelnyy-metod-ocenki-nedvizhimosti-kak-zarabotat-na-prodazhe-svoey-nedvizhimosti-v-usloviyah-krizisa'))
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.pro'))
        return keyboard


    def create_keyboard2(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('🐦‍⬛ Центральный', callback_data='cac_centr'), InlineKeyboardButton('🐦‍⬛ Фрунзенский', callback_data='cac_frunz'))
        keyboard.row(InlineKeyboardButton('🐦‍⬛ Ленинский', callback_data='cac_lenin'), InlineKeyboardButton('🐦‍⬛ Московский', callback_data='cac_moscow'))
        keyboard.row(InlineKeyboardButton('🐦‍⬛ Заводской', callback_data='cac_zavod'), InlineKeyboardButton('🐦‍⬛ Первомайский', callback_data='cac_firstmay'))
        keyboard.row(InlineKeyboardButton('🐦‍⬛ Октябрьский', callback_data='cac_october'), InlineKeyboardButton('🐦‍⬛ Советский', callback_data='cac_sovet'))
        keyboard.add(InlineKeyboardButton('🐦‍⬛ Партизанский', callback_data='cac_partiz'))
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.pro'))
        keyboard.add(InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard3() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cmrc'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        keyboard.add(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        return keyboard


    def create_keyboard4(self, street_list:list[str]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        for street in street_list:
            keyboard.add(InlineKeyboardButton(f'🔐 {street}', callback_data=f'street_{street}'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cmsc'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        return keyboard


    def create_keyboard5(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cmsc'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        return keyboard


    def create_keyboard6(self) -> InlineKeyboardMarkup:
        # sourcery skip: class-extract-method
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('🏢 Панельный', callback_data='cac_panel'), InlineKeyboardButton('🧱 Кирпичный', callback_data='cac_brick'), InlineKeyboardButton('🏛 Монолитный', callback_data='cac_monolith'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_chn'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard7(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('🏡 Хрущёвка', callback_data='cac_hrush'), InlineKeyboardButton('🏡 Брежневка', callback_data='cac_brezh'))
        keyboard.row(InlineKeyboardButton('🏡 Стандартный проект', callback_data='cac_standart'), InlineKeyboardButton('🏡 Улучшеный проект', callback_data='cac_upgrade'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_ctoh'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard8(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('🏡 Сталинка', callback_data='cac_stalin'), InlineKeyboardButton('🏡 Хрущёвка', callback_data='cac_hrush'), InlineKeyboardButton('🏡 Брежневка', callback_data='cac_brezh'))
        keyboard.row(InlineKeyboardButton('🏡 Улучшеный проект', callback_data='cac_upgrade'), InlineKeyboardButton('🏡 Стандартный проект', callback_data='cac_standart'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_ctoh'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard9(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('🏡Монолитно - кирпичный', callback_data='cac_mon_brick'))
        keyboard.add(InlineKeyboardButton('🏡Каркасно - блочный', callback_data='cac_mon_block'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_ctoh'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard10(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_ctoh'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard11(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('🔴 Доля', callback_data='cac_share'), InlineKeyboardButton('🟠 1 комн', callback_data='cac_1room'), InlineKeyboardButton('🟡 2 комн', callback_data='cac_2room'))
        keyboard.row(InlineKeyboardButton('🟢 3 комн', callback_data='cac_3room'), InlineKeyboardButton('🔵 4 комн', callback_data='cac_4room'), InlineKeyboardButton('🟣 5 и 5+ комнаты', callback_data='cac_5room'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_caoh'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard12(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cnore'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard13(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Нуждается в серьёзном ремонте', callback_data='cac_price_big_repair'))
        keyboard.add(InlineKeyboardButton('Черновая отделка', callback_data='cac_price_finishing'))
        keyboard.add(InlineKeyboardButton('Нуждается в косметическом ремонте', callback_data='cac_price_cosmetic'))
        keyboard.row(InlineKeyboardButton('Хороший ремонт', callback_data='cac_price_good'), InlineKeyboardButton('Отличный ремонт', callback_data='cac_price_perfect'))
        keyboard.add(InlineKeyboardButton('Дизайнерский ремонт',  callback_data='cac_price_design'))
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cta'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard14(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_cr'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard15(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.row(InlineKeyboardButton('◀ Назад', callback_data='cac_back_to_caor'), InlineKeyboardButton('🧨 Рестарт', callback_data='cac_restart'), InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard


    def create_keyboard16(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Ссылка на тг', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт',  url='https://domitochka.pro'))
        keyboard.add(InlineKeyboardButton('Главное меню', callback_data='menu'))
        return keyboard