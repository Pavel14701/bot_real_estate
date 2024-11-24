import g4f.Provider as Provider, os
from g4f.client import Client
from bot_instance import bot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telebot.states.sync.context import StateContext
from fsm import UserStates
from utils.utils import del_msg, update_msg_to_del, send_image, create_thread
from utils.data import ImmutableList

class ChatBot:
    MESSAGES = ImmutableList([{"role": "user", "content": os.getenv('CHATBOT_PROMPT')}])

    def chat_bot(self, chat_id:int|str, user_id:int|str, state:StateContext):
        state.set(UserStates.kuzia_chatbot)
        del_msg(chat_id, user_id)
        to_del = [send_image(chat_id, '/content/hello.jpg', 'Напишите свой вопрос и отправьте мне, а я постараюсь найти на него ответ.')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard()))
        update_msg_to_del(chat_id, user_id, to_del)


    def __send_request(self, chat_id:int|str, question:str) -> list:
        try:
            response = Client().chat.completions.create(
                model="gpt-4-turbo",
                provider = Provider.Bing,
                messages=[self.__create_message(question)]
            )
            answer = response.choices[0].message.content
            return [bot.send_message(chat_id, f'{answer}', parse_mode='Markdown')]
        except Exception as e:
            return [bot.send_message(chat_id, 'Занят, не могу говорить, можете пообщаться со специалистом.\n\
                Попробуйте повторить запрос позже.')]

    def __create_message(self, question:str) -> list:
        return self.MESSAGES[0]['content'] + question

    @bot.message_handler(state=UserStates.kuzia_chatbot)
    def chat_bot_result(self, message:Message, state:StateContext) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        state.set(UserStates.kuzia_chatbot_inf)
        del_msg(chat_id, user_id)
        create_thread(self.message_printing_notice, (chat_id,))
        to_del = self.__send_request(chat_id, message.text)
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard()))
        update_msg_to_del(chat_id, user_id, to_del)

    @bot.message_handler(state=UserStates.kuzia_chatbot_inf)
    def chat_bot_inf_result(self, message:Message, state:StateContext):
        chat_id, user_id = message.chat.id, message.from_user.id
        state.set(UserStates.kuzia_chatbot_inf)
        del_msg(chat_id, user_id)
        create_thread(self.message_printing_notice, (chat_id,))
        to_del = self.__send_request(chat_id, message.text)
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard()))
        update_msg_to_del(chat_id, user_id, to_del)

    def create_keyboard(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton('Остались вопросы ?', url='https://t.me/Pashtet_Medved'), InlineKeyboardButton('Наш сайт', url='https://domitochka.pro'))
        keyboard.add(InlineKeyboardButton('⚒ Главное меню', callback_data='menu'))
        return keyboard

    def message_printing_notice(self, chat_id:int|str) -> None:
        bot.send_chat_action(chat_id, 'typing')