import telebot
from telebot.types import Update
from flask import request
from fsm import state_storage
from configs import Configs

def create_bot_instance(state_storage:any=state_storage) -> telebot.TeleBot:
    configs = Configs()
    return telebot.TeleBot(configs['key'], state_storage=state_storage, num_threads=configs['num_threads'])


bot = create_bot_instance()

class BotWebhooks:
    app = Configs.APP

    @app.route(Configs.APP_SECRET_PATH, methods=['POST'])
    def webhook(self):
        json_str = request.get_data().decode('UTF-8')
        update = Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'OK', 200

    def run(self):
        bot.remove_webhook()
        bot.set_webhook(url=Configs.WEBHOOK_URL)
        self.app.run(
            host=Configs.APP_HOST, 
            port=Configs.APP_PORT,
            ssl_context=(
                Configs.APP_SSL_CERT,
                Configs.APP_SSL_PKEY
            )
        )
