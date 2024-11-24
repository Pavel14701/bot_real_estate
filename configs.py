from typing import Tuple, Dict, Any
from utils.middlewares import LogExceptionMiddlewareMeta
from dotenv import load_dotenv
from dataclasses import dataclass, field
from flask import Flask
from utils.utils import logger
import os

@dataclass
class Configs(meta_class=LogExceptionMiddlewareMeta):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__load_setings()
        return cls._instance

    def __get_param_list(self, key:str, _type:str='str') -> Tuple[Any]:
        if not (services_str := os.getenv(f'{key.upper()}')):
            raise ValueError(f'Missing parameters for {key.upper()}')
        match _type:
            case 'str':
                return (
                    tuple(str(services_str.split(',')))
                    if ',' in services_str
                    else (
                        str(
                            services_str,
                        )
                    )
                )
            case 'int':
                return (
                    tuple(int(services_str.split(',')))
                    if ',' in services_str
                    else (
                        int(
                            services_str,
                        )
                    )
                )
            case 'float':
                return (
                    tuple(float(services_str.split(',')))
                    if ',' in services_str
                    else (
                        float(
                            services_str,
                        )
                    )
                )
            case _:
                raise ValueError('Missing parameters for _type:')


    def __check_env_var(self, var_name:str) -> str:
        value = os.getenv(var_name.upper())
        if value is None:
            raise ValueError(f"Environment variable '{var_name.upper()}' is not set")
        return value


    def __create_postgress_uri(self) -> str:
        return f'''
        postgres+psycopg2://{self.__check_env_var('POSTGRES_USERNAME')}:
        {self.__check_env_var('POSTGRES_PASSWORD')}
        @localhost:{self.__check_env_var('POSTGRES_PORT')}
        /{self.__check_env_var('POSTGRES_NAME')}
        ''' 

    def __create_webhook_url(self) -> str:
        try:
            return f'https://{self.__check_env_var('YOUR_DOMAIN')}/{self.__check_env_var('APP_SECRET_PATH')}'
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def __load_setings(self) -> None:
        load_dotenv()
        self.settings = {
            'key': self.__check_env_var('PRIVATE_KEY'),
            'num_threads': int(self.__check_env_var('NUM_THREADS')),
            'mail_password': self.__check_env_var('MAIL_PASSWORD'),
            'mail': self.__check_env_var('MAIL'),
            'admins': self.__get_param_list('ADMINS_LIST', 'int'),
            'redis_host ': self.__check_env_var('REDIS_HOST'),
            'redis_port': int(self.__check_env_var('REDIS_PORT')),
            'redis_db': int(self.__check_env_var('REDIS_DB')),
            'postgres_uri': self.__create_postgress_uri(),
            'sqlite_uri': self.__check_env_var('SQLITE_URI'),
            'use_webhook': bool(self.__check_env_var('USE_WEBHOOKS')),\
            'webhook_url': self.__create_webhook_url(),
            'app': Flask(self.__check_env_var('APP_NAME')) or None,
            'app_secret_path': self.__check_env_var('APP_SECRET_PATH') or None,
            'app_host': self.__check_env_var('APP_HOST') or None,
            'app_port': int(self.__check_env_var('APP_PORT')) or None,
            'app_ssl_cert': self.__check_env_var('APP_SSL_CERT') or None,
            'app_ssl_pkey': self.__check_env_var('APP_SSL_PKEY') or None
        }

    def load_settings(self) -> Dict[Any]:
        return self.settings

    PRIVATE_KEY:str=field(default=load_settings()['key'], init=False)
    NUM_THREADS:int=field(default=load_settings()['num_threads'], init=False)
    MAIL:str=field(default=load_settings()['mail'], init=False)
    MAIL_PASSWORD:str=field(default=load_settings()['mail_password'], init=False)
    ADMINS:list[str]=field(default=load_settings()['admins'], init=False)
    REDIS_HOST:str=field(default=load_settings()['redis_host'], init=False)
    REDIS_PORT:int=field(default=load_settings()['redis_port'], init=False)
    REDIS_DB:int=field(default=load_settings()['redis_db'], init=False)
    SQLITE_URI:str=field(default=load_settings()['sqlite_uri'], init=False)
    POSTGRES_URI:str=field(default=load_settings()['postgres_uri'], init=False)
    USE_WEBHOOK:bool=field(default=load_settings()['use_webhooks'], init=False)
    WEBHOOK_URL:str=field(default=load_settings()['webhook_url'], init=False)
    APP:Flask=field(default=load_settings()['app'], init=False)
    APP_HOST:str=field(default=load_settings()['app_host'], init=False)
    APP_PORT:int=field(default=load_settings()['app_port'], init=False)
    APP_SECRET_PATH:str=field(default=load_settings['app_secret_path'], init=False)
    APP_SSL_CERT=field(default=load_settings['app_ssl_cert'], init=False)
    APP_SSL_PKEY=field(default=load_settings['app_ssl_pkey'], init=False)