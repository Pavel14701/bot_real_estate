import telebot, json, telebot, redis
from typing import Any, Optional
from telebot.handler_backends import State, StatesGroup
from redis.connection import ConnectionPool
from telebot.storage import StateRedisStorage
from telebot.states import State, StatesGroup
from bot_instance import bot
from utils.middlewares import LogExceptionMiddlewareMeta
from configs import Configs
from utils.data import UserData


class RedisCache(Configs, meta_class=LogExceptionMiddlewareMeta):
    def __init__(self, bot:telebot.TeleBot=bot):
        self.bot = bot
        self.bot_id = self.bot.bot_id
        Configs.__init__(self)
        settings = self.load_settings()
        self.pool = ConnectionPool(host=settings['redis_host'], port=settings['redis_port'], db=settings['redis_db'])

    def __worker(self):
        return redis.Redis(connection_pool=self.pool)

    def set_value(self, user_id:int, chat_id:int, key:Optional[str]=None, value:Any=None) -> None:
        conn = self.__worker()
        with conn as cache:
            id_key = f'{self.bot_id}_{user_id}_{chat_id}'
            if key:
                existing_data = cache.get(id_key)
                existing_data = json.loads(existing_data) if existing_data else {}
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

    def __create_user_data(self, json_data:bytes) -> UserData:
        user_data:dict = json.loads(json_data)
        return UserData(
            chosen_region_name=user_data.get('chosen_region_name', ''),
            chosen_street_name=user_data.get('chosen_street_name', ''),
            house_info1=user_data.get('house_info1', ''),
            house_info2=user_data.get('house_info2', ''),
            number_of_rooms=user_data.get('number_of_rooms', 0),
            cac_age=user_data.get('cac_age', 0),
            area=user_data.get('area', 0),
            price_of_finishing=user_data.get('price_of_finishing', 0),
            repair_coef=user_data.get('repair_coef', 0),
            furniture_cost=user_data.get('furniture_cost', 0)
        )

    def get_values(self, user_id: int, chat_id: int, l2:bool=False) -> dict|UserData:
        conn = self.__worker()
        with conn as cache:
            if l2:
                id_key = f'{self.bot_id}_{user_id}_{chat_id}_l2'
                if json_data := cache.get(id_key):
                    return json.loads(json_data)
            id_key = f'{self.bot_id}_{user_id}_{chat_id}'
            if json_data := cache.get(id_key):
                return self.__create_user_data(json_data)

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

    def get_all_reminder_states(self) -> dict:
        conn = self.__worker()
        with conn as cache:
            key = f'{self.bot_id}_reminder_states'
            if json_data := cache.get(key):
                return json.loads(json_data)


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


def get_state_redis_storage() -> StateRedisStorage:
    settings = Configs().load_settings()
    return StateRedisStorage(
        host=settings['redis_host'],
        port=settings['redis_port'],
        db=settings['redis_db']
    )


state_storage = get_state_redis_storage()
cache_storage = RedisCache(bot)