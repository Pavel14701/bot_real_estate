from datetime import datetime
from bot_instance import bot
from fsm import cache_storage
from telebot.types import Message
from telebot.states.sync.context import StateContext
from main_types import MainTypes
from datasets.user import User
from utils.utils import del_msg, create_thread, update_msg_to_del


def menu(message:Message, state:StateContext) -> None:
    state.delete()
    chat_id, user_id = message.chat.id, message.from_user.id
    del_msg(chat_id, user_id)
    cache_storage.set_value(user_id, chat_id, 'reminder_states', 'completed')
    time = datetime.now()
    user_data={
        'chat_id': chat_id, 'user_id': user_id,
        'first_name': message.from_user.first_name, 'last_name': message.from_user.last_name,
        'start_time': time, 'last_update': time
    }
    create_thread(target=User().add_user_to_base, args=(user_data,), daemon=True)
    with open("./content/hello.jpg", "rb") as img1:
        to_del = [bot.send_photo(
            chat_id, img1, caption=f'Привет {message.from_user.first_name} {message.from_user.last_name},\
                меня зовут Кузя и я помогу вам с решением различных задач, связанных с недвижимостью.\
                    Я могу проанализировать прибыльность сдачи квартиры в аренду, оценить рыночную\
                        стоимость и рассчитать стоимость риэлторских услуг.'
            )
        ]
    to_del.append(bot.send_message(chat_id, "Выберите один из вариантов:", reply_markup=MainTypes().create_keyboard()))
    update_msg_to_del(chat_id, user_id, to_del)