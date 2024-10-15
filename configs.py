from typing import Tuple, Dict, Any
from dotenv import load_dotenv
import os

class ConfigsProvider:
    _instance = None


    def __get_param_list(self, key:str) -> Tuple[Any]:
        if services_str := os.getenv(f'{key.upper()}'):
            return tuple(services_str.split(',')) if ',' in services_str else (services_str,)
        else:
            raise ValueError(f'Missing parameters for {key.upper()}')


    def __check_env_var(self, var_name:str) -> str:
        value = os.getenv(var_name.upper())
        if value is None:
            raise ValueError(f"Environment variable '{var_name.upper()}' is not set")
        return value


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__load_setings()
        return cls._instance


    def __load_setings(self) -> None:
        load_dotenv()
        self.settings = {
            'key': self.__check_env_var('PRIVATE_KEY'),
            'num_threads': int(self.__check_env_var('NUM_THREADS')),
            'mail_password': self.__check_env_var('MAIL_PASSWORD'),
            'mail': self.__check_env_var('MAIL'),
            'admins': self.__get_param_list('ADMINS_LIST')
            }


    def load_settings(self) -> Dict[Any]:
        return self.settings