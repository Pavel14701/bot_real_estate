import contextlib, logging
from typing import Optional, Union, List
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot_instance import bot
from fsm import cache_storage


def update_msg_to_del(chat_id:int, user_id:int, msg:Union[Message, List[Message]]):
    obj_type = isinstance(msg)
    key = 'msg_del'
    if obj_type == list:
        id = []
        for message in msg:
            id.append(message.message_id)
    else:
        id = msg.message_id
    value = {'chat_id':msg.chat.id, 'message_id': id}
    cache_storage.set_value(chat_id, user_id, key, value)


def del_msg(chat_id:int, user_id:int, return_state_data:bool=False) -> Optional[dict]:
    msg = cache_storage.get_value(chat_id, user_id).get('msg_del')
    with contextlib.suppress():
        if isinstance(msg['message_id']) == list:
            for message in msg['message_id']:
                bot.delete_message(int(msg['chat_id']), message)
        bot.delete_message(int(msg['chat_id']), msg['message_id'])
    if return_state_data:
        return msg


def quick_inline_keyboard(**kwargs):
    inline_markup = InlineKeyboardMarkup(row_width=2)
    for callback_data, text in kwargs.items():
        button = InlineKeyboardButton(text=str(text), callback_data=str(callback_data))
        inline_markup.add(button)
    return inline_markup


def create_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('mkb_order_bot.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = create_logger()