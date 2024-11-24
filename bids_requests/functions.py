import os
from datetime import datetime
from email.mime.text import MIMEText
from smtplib import SMTP
from bot_instance import bot
from utils.utils import run_in_thread
from utils.data import UserBid
from utils.middlewares import LogExceptionMiddlewareMeta


class EmailTgSendler(meta=LogExceptionMiddlewareMeta):
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')#'smtp.gmail.com'
        self.smtp_port = int(os.getenv('SMTP_PORT'))#587
        self.smtp_user = os.getenv('MAIL')
        self.smtp_password = os.getenv('MAIL_PASSWORD')

    def send_email(self, subject, message, to_email):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = to_email
        server = SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_user, self.smtp_password)
        server.sendmail(self.smtp_user, to_email, msg.as_string())
        server.quit()

    def __get_admins_list(self, admin_type:str) -> list:
        admins_str = os.getenv(admin_type)
        return admins_str.split(',') if ',' in admins_str else [admins_str]

    @property
    def admins_tg(self) -> list:
        return self.__get_admins_list('ADMINS_TG')

    @property
    def admins_email(self) -> list:
        return self.__get_admins_list('ADMINS_EMAIL')

    def __check_service_type(self, type_of_service:str) -> str:
        match type_of_service:
            case 'sell':
                return 'Продажа недвижимости'
            case 'buy':
                return 'Покупка или побор недвижимости'
            case 'docs':
                return 'Помощь в оформлении документов'

    @run_in_thread
    def register_bid_email_tg(self, bid:UserBid, type_of_service:str, question:str|None) -> None:
        form = f'**Новая заявка от бота**\n\n\
            Дата заявки: {datetime.now()}\n\n\
            Номер телефона:{bid.phone}\n\n\
            Тип услуги: {self.__check_service_type(type_of_service)}\n\n\
            Как подписан в тг:{bid.name.upper()} {bid.surname.upper()}\n\n\
            Ссылка на профиль: {bid.user_link}\n\n\
            Вопрос: {question or 'без вопроса'}',
        for email, admin_id in zip(self.admins_email, self.admins_tg):
            self.send_email('Новый Лид Бот', form, email)
            bot.send_message(admin_id, form, parse_mode='Markdown')