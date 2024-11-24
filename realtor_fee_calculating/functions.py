from decimal import Decimal
import requests
from fsm import cache_storage
from consts import Consts
from utils.utils import logger

class FeeCalculatingFunctions:
    def __init__(self, chat_id:int|str, user_id:int|str) -> None:
        self.chat_id = chat_id
        self.user_id = user_id


    def __get_currency_rates(self) -> Decimal:
        cf_chosen_currency = cache_storage.get_value(self.user_id, self.chat_id, 'cf_chosen_currency')
        rates = requests.get(Consts.currency_api).json()
        cf_currency = None
        for rate in rates:
            if rate['Cur_Abbreviation'] == cf_chosen_currency:
                if cf_chosen_currency in ['USD', 'EUR']:
                    cf_currency = Decimal(rate['Cur_OfficialRate'])
                elif cf_chosen_currency == 'RUB':
                    cf_currency = Decimal(rate['Cur_OfficialRate']) / Decimal('100')
                elif cf_chosen_currency == 'CNY':
                    cf_currency = Decimal(rate['Cur_OfficialRate']) / Decimal('10')
                break
            if cf_chosen_currency == 'BYN':
                cf_currency = Decimal('1')
        return cf_currency


    def __calculate_fee_percentage(self, price_in_base_values:int) -> Decimal:
        if price_in_base_values <= 4200:
            return Decimal('0.03')
        elif 4200 < price_in_base_values <= 5000:
            return Decimal('0.025')
        elif 5000 < price_in_base_values <= 5800:
            return Decimal('0.024')
        elif 5800 < price_in_base_values <= 6600:
            return Decimal('0.023')
        elif 6600 < price_in_base_values <= 7500:
            return Decimal('0.022')
        elif 7500 < price_in_base_values <= 8300:
            return Decimal('0.021')
        elif 8300 < price_in_base_values <= 9100:
            return Decimal('0.02')
        elif 9100 < price_in_base_values <= 10000:
            return Decimal('0.019')
        elif 10000 < price_in_base_values <= 10500:
            return Decimal('0.018')
        elif 10500 < price_in_base_values <= 11600:
            return Decimal('0.017')
        elif 11600 < price_in_base_values <= 12400:
            return Decimal('0.016')
        elif 12400 < price_in_base_values <= 13200:
            return Decimal('0.015')
        elif 13200 < price_in_base_values <= 14000:
            return Decimal('0.014')
        elif 14000 < price_in_base_values <= 15000:
            return Decimal('0.013')
        elif 14900 < price_in_base_values <= 15700:
            return Decimal('0.012')
        elif 15700 < price_in_base_values <= 16500:
            return Decimal('0.011')
        else:
            return Decimal('0.01')


    def calculate_fee(self) -> dict:
        try:
            cf_currency = self.__get_currency_rates(self.chat_id)
            cf_price = cache_storage.get_value(self.user_id, self.chat_id, 'cf_price')
            price_in_base_values = int(cf_price * cf_currency / Consts.base_value)
            cf_percent = self.__calculate_fee_percentage(price_in_base_values)
            return {
                'cf_fee': cf_price * cf_percent,
                'cf_percent': cf_percent
            }
        except Exception as e:
            logger.error(e)
            return {'cf_fee': None, 'cf_percent': None}