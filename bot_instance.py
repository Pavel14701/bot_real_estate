import telebot
from fsm import state_storage
from configs import ConfigsProvider

def create_bot_instance():
    configs = ConfigsProvider()
    return telebot.TeleBot(configs['key'], state_storage=state_storage, num_threads=configs['num_threads'])

bot = create_bot_instance()