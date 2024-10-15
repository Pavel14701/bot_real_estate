import telebot, pickle, os
from telebot.handler_backends import State, StatesGroup
from dotenv import load_dotenv
load_dotenv()



import os, json, telebot, redis
from redis.connection import ConnectionPool
from typing import Any, Optional
from telebot.storage import StateRedisStorage
from telebot.states import State, StatesGroup
from bot_instance import bot


state_storage = StateRedisStorage(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')))


class RedisCache:
    def __init__(self, bot:telebot.TeleBot=bot):
        self.bot = bot
        self.bot_id = self.bot.bot_id
        self.pool = ConnectionPool(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')))


    def __worker(self):
        return redis.Redis(connection_pool=self.pool)


    def set_value(self, user_id:int, chat_id:int, key:Optional[str]=None, value:Any=None) -> None:
        conn = self.__worker()
        with conn as cache:
            id_key = f'{self.bot_id}_{user_id}_{chat_id}'
            if key:
                existing_data = cache.get(id_key)
                if existing_data:
                    existing_data = json.loads(existing_data)
                else:
                    existing_data = {}
                existing_data[key] = value
                cache.set(id_key, json.dumps(existing_data))
            else:
                cache.set(f'{id_key}_l2', json.dumps(value))


    def get_value(self, user_id: int, chat_id: int, key:str) -> Any:
        conn = self.__worker()
        with conn as cache:
            id_key = f'{self.bot_id}_{user_id}_{chat_id}'
            if json_data := cache.get(id_key):
                data = json.loads(json_data)
                return data[key]


    def get_values(self, user_id: int, chat_id: int, l2:bool=False) -> Any:
        conn = self.__worker()
        with conn as cache:
            if l2:
                id_key = f'{self.bot_id}_{user_id}_{chat_id}_l2'
            id_key = f'{self.bot_id}_{user_id}_{chat_id}'
            if json_data := cache.get(id_key):
                return json.loads(json_data)


    def delete_all_user_values(self, user_id:int, chat_id:int) -> None:
        conn = self.__worker()
        with conn as cache:
            id_keys = [f'{self.bot_id}_{user_id}_{chat_id}', f'{self.bot_id}_{user_id}_{chat_id}_l2']
            for key in id_keys:
                cache.delete(key)


    def delete_value(self, user_id:int, chat_id:int, key:str) -> None:
        conn = self.__worker()
        with conn as cache:
            id_key = f'{self.bot_id}_{user_id}_{chat_id}'
            if json_data := cache.get(id_key):
                data = json.loads(json_data)
                data[key]=None
                cache.set(id_key, json.dumps(data))


    def get_all_reminder_states(self):
        conn = self.__worker()
        with conn as cache:
            key = f'{self.bot_id}_reminder_states'
            if json_data := cache.get(key):
                return json.loads(json_data)


cache_storage = RedisCache()


# Определение группы состояний
class UserStates(StatesGroup):
    waiting_for_street_choice = State()
    result_street_choice = State()
    waiting_for_type_of_house = State()
    waiting_age_of_house = State()
    waiting_area_of_house = State()
    waiting_age_of_repair = State()
    waiting_price_of_furniture = State()
    waiting_price_for_fee = State()
    waiting_price_of_house_for_rent = State()
    waiting_apartment_area_for_rent = State()
    waiting_forcast_period_for_rent = State()
    waiting_rental_price_for_rent = State()
    waiting_maintance_cost_for_rent = State()
    kuzia_chatbot_inf = State()
    kuzia_chatbot = State()
    waiting_contact_data_sell = State()
    waiting_question_services = State()
