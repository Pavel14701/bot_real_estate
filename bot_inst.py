import telebot, pickle, os
from telebot.handler_backends import State, StatesGroup
from dotenv import load_dotenv
load_dotenv()

# Класс для хранения состояний с помощью pickle
class PickleStorage(telebot.StateStorageBase):
    def __init__(self, filename='bot_states.pickle'):
        self.filename = filename
        if not os.path.isfile(self.filename):
            with open(self.filename, 'wb') as file:
                pickle.dump({}, file)

    def get_value(self, key):
        with open(self.filename, 'rb') as file:
            states = pickle.load(file)
        return states.get(key, None)

    def set_value(self, key, value):
        with open(self.filename, 'rb') as file:
            states = pickle.load(file)
        states[key] = value
        with open(self.filename, 'wb') as file:
            pickle.dump(states, file)

    def delete_value(self, key):
        with open(self.filename, 'rb') as file:
            states = pickle.load(file)
        if key in states:
            del states[key]
            with open(self.filename, 'wb') as file:
                pickle.dump(states, file)

    def get_all_reminder_states(self):
        with open(self.filename, 'rb') as file:
            states = pickle.load(file)
        reminder_states = {key.replace('reminder_states:', ''): value for key, value in states.items() if key.startswith('reminder_states:')}
        return reminder_states


# Определение группы состояний
class UserState(StatesGroup):
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
    
# Инициализация бота с PickleStorage
state_storage = PickleStorage()
bot = telebot.TeleBot(os.getenv('PRIVATE_KEY'), state_storage=state_storage, num_threads=20)