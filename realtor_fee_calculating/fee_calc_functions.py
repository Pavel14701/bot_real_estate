from decimal import Decimal
import requests
from fsm import cache_storage
from consts import BASE_VALUE, CURRENCY_API


# РЕАЛИЗАЦИЯ ФОРМУЛ ДЛЯ РАССЧЁТА КОМИССИИ
def get_currency_rates(chat_id, user_id):
    cf_chosen_currency = cache_storage.get_value(user_id, chat_id, 'cf_chosen_currency')
    response = requests.get(CURRENCY_API)
    rates = response.json()
    cf_currency = None
    for rate in rates:
        if rate['Cur_Abbreviation'] == cf_chosen_currency:
            if cf_chosen_currency == 'RUB':
                cf_currency = Decimal(rate['Cur_OfficialRate']) / 100
            elif cf_chosen_currency == 'CNY':
                cf_currency = Decimal(rate['Cur_OfficialRate']) / 10
            elif cf_chosen_currency == 'USD':
                cf_currency = Decimal(rate['Cur_OfficialRate'])
            elif cf_chosen_currency == 'EUR':
                cf_currency = Decimal(rate['Cur_OfficialRate'])
            break
        if cf_chosen_currency == 'BYN':
            cf_currency = Decimal('1')
    return cf_currency


def calculate_fee(chat_id, user_id):
    cf_currency = get_currency_rates(chat_id)
    cf_price = cache_storage.get_value(user_id, chat_id, 'cf_price')
    price_in_base_values = round(cf_price * cf_currency / BASE_VALUE)
    if price_in_base_values <= 4200:
        cf_percent = Decimal("0.03")
    elif 4200 < price_in_base_values <= 5000:
        cf_percent = Decimal("0.025")
    elif 5000 < price_in_base_values <= 5800:
        cf_percent = Decimal("0.024")
    elif 5800 < price_in_base_values <= 6600:
        cf_percent = Decimal("0.023")
    elif 6600 < price_in_base_values <= 7500:
        cf_percent = Decimal("0.022")
    elif 7500 < price_in_base_values <= 8300:
        cf_percent = Decimal("0.021")
    elif 8300 < price_in_base_values <= 9100:
        cf_percent = Decimal("0.02")
    elif 9100 < price_in_base_values <= 10000:
        cf_percent = Decimal("0.019")
    elif 10000 < price_in_base_values <= 10500:
        cf_percent = Decimal("0.018")
    elif 10500 < price_in_base_values <= 11600:
        cf_percent = Decimal("0.017")
    elif 11600 < price_in_base_values <= 12400:
        cf_percent = Decimal("0.016")
    elif 12400 < price_in_base_values <= 13200:
        cf_percent = Decimal("0.015")
    elif 13200 < price_in_base_values <= 14000:
        cf_percent = Decimal("0.014")
    elif 14000 < price_in_base_values <= 15000:
        cf_percent = Decimal("0.013")
    elif 14900 < price_in_base_values <= 15700:
        cf_percent = Decimal("0.012")
    elif 15700 < price_in_base_values <= 16500:
        cf_percent = Decimal("0.011")
    else:
        cf_percent = Decimal("0.01")
    cf_fee = cf_price * cf_percent
    return cf_fee, cf_percent