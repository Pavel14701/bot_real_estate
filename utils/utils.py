from decimal import Decimal
from logging.handlers import TimedRotatingFileHandler
import contextlib, logging, threading, os, time
from multiprocessing import Queue, Process
from datetime import datetime
from functools import wraps
from typing import Optional, Tuple, Union, List, Any
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, Message
from bot_instance import bot
from fsm import cache_storage


def run_in_thread(func:function):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper


def update_msg_to_del(self, chat_id:int, user_id:int, msg:Union[Message, List[Message]], flag:bool=False) -> None:
    # sourcery skip: avoid-builtin-shadow
    obj_type = isinstance(msg)
    key = 'msg_del_thread' if flag else 'msg_del'
    if obj_type == list:
        id = [message.message_id for message in msg]
    else:
        id = msg.message_id
    value = {'chat_id':msg.chat.id, 'message_id': id}
    cache_storage.set_value(chat_id, user_id, key, value)


def del_msg(self, chat_id:int, user_id:int, flag:bool=False, return_state_data:bool=False) -> Optional[dict]:
    key = 'msg_del_thread' if flag else 'msg_del'
    msg = cache_storage.get_value(chat_id, user_id).get(key)
    with contextlib.suppress():
        if isinstance(msg['message_id']) == list:
            for message in msg['message_id']:
                bot.delete_message(int(msg['chat_id']), message)
        bot.delete_message(int(msg['chat_id']), msg['message_id'])
    if return_state_data:
        return msg


def quick_inline_keyboard(self, **kwargs) -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardMarkup(row_width=2)
    for callback_data, text in kwargs.items():
        button = InlineKeyboardButton(text=str(text), callback_data=str(callback_data))
        inline_markup.add(button)
    return inline_markup


@run_in_thread()
def create_msg_thread(self, chat_id:int, user_id:int, message:str, cache_key:str|None, value:str|int|float|Decimal|None, lag:int=5) -> None:
    to_del:list = [bot.send_message(chat_id, message, parse_mode='Markdown')]
    self.update_msg_to_del(chat_id, user_id, to_del, True)
    if cache_key and value:
        cache_storage.set_value(user_id, chat_id, cache_key, value)
    time.sleep(lag)
    self.del_msg(chat_id, user_id, True)


def send_image(self, chat_id:int, path:str, message:str|None, reply_markup:any=None) -> Message:
    with open(path, 'rb') as img:
        if message:
            return bot.send_photo(chat_id, img, caption=message, parse_mode='Markdown', reply_markup=reply_markup)
        return bot.send_photo(chat_id, img)

def create_logger(logger_name:str) -> logging.Logger:
    if not os.path.exists('Logs'):
        os.makedirs('Logs')
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    log_filename = os.path.join('Logs', f'{logger_name}_{datetime.now().strftime("%Y-%m-%d")}.log')
    handler = TimedRotatingFileHandler(
        filename=log_filename, encoding='utf-8', when='midnight',
        interval=1, backupCount=7
    )
    handler.suffix = '%Y-%m-%d'
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger


def create_thread(target:function, *args:any, daemon:bool):
    thread = threading.Thread(target=target, args=args, daemon=daemon)
    thread.start()


def decorate_all_methods(decorator, functions_names: Optional[Tuple[str]] = None):
    # sourcery skip: merge-nested-ifs
    def decorate(cls):
        for attr in dir(cls):
            if callable(getattr(cls, attr)) and not attr.startswith("__"):
                if functions_names is None or attr in functions_names:
                    setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


def queue_wrapper(queue:Queue, target_function:function, *args, **kwargs) -> None:
    result = target_function(*args, **kwargs)
    queue.put(result)


def run_in_new_process(target_function:function, *args, **kwargs) -> Any:
    queue = Queue()
    process = Process(target=queue_wrapper, args=(queue, target_function, *args), kwargs=kwargs)
    process.start()
    process.join()
    return queue.get()

logger=create_logger('bot_real_estate_logs')

def log_exceptions(func:function):
    @wraps(func)
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {function_name}: {e}", exc_info=True)
            print(e)
    return wrapper