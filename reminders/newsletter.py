import time, random, contextlib, schedule, threading
from datetime import datetime
from bot_instance import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException
from datasets.database import User
from fsm import cache_storage
from utils.utils import send_image

class SendReminders:
    #TO DO create table in database and add specific data into database,
    #create methods for this data returning at database
    urls=[
        'https://vc.ru/u/1529738-pashtet-medved/806795-kak-prodat-kvartiru-za-rekordnuyu-cenu-ispolzuem-dizayn-socseti-i-kontent',
        'https://vc.ru/u/1529738-pashtet-medved/803809-dohodnyy-analiz-ceny-kak-prodat-po-maksimumu-kommercheskuyu-nedvizhimost-i-zhile-pod-arendu',
        'https://vc.ru/u/1529738-pashtet-medved/812682-kak-provesti-analiz-rynka-nedvizhimosti-poshagovoe-rukovodstvo-dlya-investorov-pokupateley-i-prodavcov',
        'https://vc.ru/u/1529738-pashtet-medved/883502-dohodnyy-sposob-ocenki-nedvizhimosti-s-ispolzovaniem-zakona-metkalfa',
        'https://vc.ru/u/1529738-pashtet-medved/801207-zatratnyy-metod-ocenki-nedvizhimosti-kak-uznat-cenu-nizhe-kotoroy-prodavat-nelzya'
    ]
    images=[
        './content/mail/1.jpg', './content/mail/2.jpg',
        './content/mail/3.jpg', './content/mail/4.jpg',
        './content/mail/5.jpg'
    ]

    def messages(self, user:User) -> list:
        return [
            f'Добрый вечер, {user.first_name} {user.last_name}!\n Мы подготовили статью о том \
                насколько важна \широкая, а главное грамотная рекламная кампания при продаже \
                недвижимости.\n С ней вы можете ознакомится по ссылке ниже',
            f'{user.first_name} {user.last_name}, добрый вечер. У меня снова для вас порция \
                развивающий информации, на этот раз мы затронем оценку недвижимости \n доходным \
                способом, он позволяет не только рассчитать стоимость, но и вычислить \n прибыльность \
                сдачи недвижимости в аренду. Ссылка ниже ...',
            f'И снова здравствуйте, {user.first_name} {user.last_name}! \n Не хотите взглянуть на материал \
                о том как научится оценивать перспективы на рынке недвижимости? \n Если горите желанием, \
                ссылочка будет ниже.',
            f'Как вам вечер, {user.first_name} {user.last_name}?\n Не хотите скоратать его за прочтением \
                чего-то интересного?\n Там у нас есть замечательный материал о нестандартном методе оценки, \
                если что ссылка как всегда ниже...',
            f'Я вам не помешал, {user.first_name} {user.last_name}? У меня для вас шикарное предложение, не \
                хотите скоротать полчасика \n за прочтением хорошего материала о том как оценить \
                недвижимость по её характеристикам. И да ссылочка снизу.'
        ]


    def send_mailing(self) -> None:
        try:
            users:list[User] = User.return_all_users()
            for user in users:
                if user.active and user.messages < len(self.images):
                    send_image(user.chat_id, self.images[user.messages], self.messages[user.messages], self.create_keyboard(self.urls[user.messages]))
                    user.messages += 1
        except ApiTelegramException:
            user.active = False


    def create_keyboard(self, url:str) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Открыть статью', url=url))
        return keyboard

    def send_reminders(self) -> None:
        reminder_states = cache_storage.get_all_reminder_states()
        for chat_id, state in reminder_states.items():
            with contextlib.suppress(ApiTelegramException):
                match state:
                    case 'cac_started':
                        message = 'Похоже, вы забыли обо мне😥! Чем я могу помочь сегодня?'
                    case 'cac_in_progress':
                        message = 'Я заметил, что вы не завершили ваш запрос. Есть что-то, в чем я могу помочь?'
                    case 'r_in_started':
                        message = 'Похоже, вы забыли обо мне😥! Чем я могу помочь сегодня?'
                    case 'r_in_progress':
                        message = 'Я заметил, что вы не завершили ваш запрос. Есть что-то, в чем я могу помочь?'
                bot.send_message(chat_id, message)

    def schedule_message_sending(self):
        hour = random.randint(18, 20)
        minute = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}"
        schedule.every(2).days.at(time_str).do(self.send_mailing)

    def reschedule_message_sending(self):
        schedule.clear(self.send_mailing)
        self.schedule_message_sending()

    schedule_message_sending()
    schedule.every(2).days.at("21:01").do(reschedule_message_sending)
    schedule.every(3).hours.do(send_reminders)
    schedule.every(2).days.at("18:00").do(send_mailing)

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()