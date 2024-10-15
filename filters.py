from bot_instance import bot
from telebot.types import CallbackQuery
from fsm import cache_storage


@bot.callback_query_handler(func=lambda call: True)
def handle_keyboard(call:CallbackQuery):
    data = call.data
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    if data == "rent":
        r_send_greeting(chat_id, user_id)
    elif data == "price":
        send_greeting_cac(chat_id, user_id)
    elif data == "analytics":
        send_greeting(chat_id, user_id)
    elif data == "search":
        send_greeting(chat_id, user_id)
    elif data == "services":
        services(chat_id, user_id)
    elif data == "kuzia_chatbotai":
        chat_bot(chat_id, user_id)
    elif data == 'menu':
        menu(chat_id, user_id)
    elif data == 'cac_restart':
        cac_func_restart(chat_id, user_id)
    elif data == 'cac_calculate_results':
        cac_calculate_results(chat_id, user_id)
    elif data == 'cac_minsk_region_entry':
        cac_minsk_region_choice(chat_id, user_id)
    elif data == 'cac_centr':
        bot.send_message(chat_id, 'Вы выбрали Центральный район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Центральный район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data == 'cac_frunz':
        bot.send_message(chat_id, 'Вы выбрали Фрунзенский район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Фрунзенский район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data == 'cac_lenin':
        bot.send_message(chat_id, 'Вы выбрали Ленинский район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Ленинский район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data == 'cac_moscow':
        bot.send_message(chat_id, 'Вы выбрали Московский район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Московский район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data == 'cac_zavod':
        bot.send_message(chat_id, 'Вы выбрали Заводской район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Заводской район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data == 'cac_firstmay':
        bot.send_message(chat_id, 'Вы выбрали Первомайский район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Первомайский район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data == 'cac_october':
        bot.send_message(chat_id, 'Вы выбрали Октябрьский район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Октябрьский район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data == 'cac_sovet':
        bot.send_message(chat_id, 'Вы выбрали Советский район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Советский район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data == 'cac_partiz':
        bot.send_message(chat_id, 'Вы выбрали Партизанский район')
        cac_minsk_street_choice(chat_id, user_id)
        chosen_region_name = "Партизанский район"
        cache_storage.set_value(f'chosen_region_name:{chat_id}', chosen_region_name)
    elif data.startswith('street_'):
        street = data[7:]
        bot.send_message(chat_id, f'Вы выбрали вариант: {street}')
        cac_house_number(chat_id, user_id)
        chosen_street_name = street
        cache_storage.set_value(f'chosen_street_name:{chat_id}', chosen_street_name)
    elif data == 'cac_panel':
        house_info1 = "panel"
        bot.send_message(chat_id, 'Вы выбрали панельный тип дома.')
        cac_type_panel(chat_id, user_id)
        cache_storage.set_value(f'house_info1:{chat_id}', house_info1)
    elif data == 'cac_monolith':
        house_info1 = "monolith"
        bot.send_message(chat_id, 'Вы выбрали монолитный тип дома.')
        cac_type_monolith(chat_id, user_id)
        cache_storage.set_value(f'house_info1:{chat_id}', house_info1)
    elif data == 'cac_brick':
        house_info1 = "brick"
        bot.send_message(chat_id, 'Вы выбрали кирпичный тип дома.')
        cac_type_brick(chat_id, user_id)
        cache_storage.set_value(f'house_info1:{chat_id}', house_info1)
    elif data == 'cac_hrush':
        house_info2 = "hrush"
        bot.send_message(chat_id, 'Вы выбрали проект типа "хрущёвка".')
        cac_age_of_house(chat_id, user_id)
        cache_storage.set_value(f'house_info2:{chat_id}', house_info2)
    elif data == 'cac_brezh':
        house_info2 = "brezh"
        bot.send_message(chat_id, 'Вы выбрали проект типа "брежневка".')
        cac_age_of_house(chat_id, user_id)
        cache_storage.set_value(f'house_info2:{chat_id}', house_info2)
    elif data == 'cac_standart':
        house_info2 = "standart"
        bot.send_message(chat_id, 'Вы выбрали стандартный тип проекта.')
        cac_age_of_house(chat_id, user_id)
        cache_storage.set_value(f'house_info2:{chat_id}', house_info2)
    elif data == 'cac_upgrade':
        house_info2 = "upgrade"
        bot.send_message(chat_id, 'Вы выбрали улучшенный тип проекта.')
        cac_age_of_house(chat_id, user_id)
        cache_storage.set_value(f'house_info2:{chat_id}', house_info2)
    elif data == 'cac_stalin':
        house_info2 = "stalin"
        bot.send_message(chat_id, 'Вы выбрали проект типа "Сталинка".')
        cac_age_of_house(chat_id, user_id)
        cache_storage.set_value(f'house_info2:{chat_id}', house_info2)
    elif data == 'cac_mon_panel':
        house_info2 = "mon_panel"
        bot.send_message(chat_id, 'Вы выбрали монолитно-панельный тип дома.')
        cac_age_of_house(chat_id, user_id)
        cache_storage.set_value(f'house_info2:{chat_id}', house_info2)
    elif data == 'cac_mon_brick':
        house_info2 = "mon_brick"
        bot.send_message(chat_id, 'Вы выбрали каркасно-кирпичный тип дома.')
        cac_age_of_house(chat_id, user_id)
        cache_storage.set_value(f'house_info2:{chat_id}', house_info2)
    elif data == 'cac_mon_block':
        house_info2 = "mon_block"
        bot.send_message(chat_id, 'Вы выбрали каркасно-блочный тип дома.')
        cac_age_of_house(chat_id, user_id)
        cache_storage.set_value(f'house_info2:{chat_id}', house_info2)
    elif data == 'cac_share':
        bot.send_message(chat_id, 'Вы выбрали вариант: доля.')
        cac_total_area(chat_id, user_id)
        number_of_rooms = 0
        cache_storage.set_value(f'number_of_rooms:{chat_id}', number_of_rooms)
    elif data == 'cac_1room':
        bot.send_message(chat_id, 'Вы выбрали вариант: 1-комн.')
        cac_total_area(chat_id, user_id)
        number_of_rooms = 1
        cache_storage.set_value(f'number_of_rooms:{chat_id}', number_of_rooms)
    elif data == 'cac_2room':
        bot.send_message(chat_id, 'Вы выбрали вариант: 2-комн.')
        cac_total_area(chat_id, user_id)
        number_of_rooms = 2
        cache_storage.set_value(f'number_of_rooms:{chat_id}', number_of_rooms)
    elif data == 'cac_3room':
        bot.send_message(chat_id, 'Вы выбрали вариант: 3-комн.')
        cac_total_area(chat_id, user_id)
        number_of_rooms = 3
        cache_storage.set_value(f'number_of_rooms:{chat_id}', number_of_rooms)
    elif data == 'cac_4room':
        bot.send_message(chat_id, 'Вы выбрали вариант: 4-комн.')
        cac_total_area(chat_id, user_id)
        number_of_rooms = 4
        cache_storage.set_value(f'number_of_rooms:{chat_id}', number_of_rooms)
    elif data == 'cac_5room':
        bot.send_message(chat_id, 'Вы выбрали вариант: 5+-комн.')
        cac_total_area(chat_id, user_id)
        number_of_rooms = 5
        cache_storage.set_value(f'number_of_rooms:{chat_id}', number_of_rooms)
    elif data == 'cac_price_finishing':
        price_of_finishing = "price_finishing"
        cac_age_of_repair(chat_id, user_id)
        cache_storage.set_value(f'price_of_finishing:{chat_id}', price_of_finishing)
    elif data == 'cac_price_big_repair':
        price_of_finishing = "price_big_repair"
        cac_age_of_repair(chat_id, user_id)
        cache_storage.set_value(f'price_of_finishing:{chat_id}', price_of_finishing)
    elif data == 'cac_price_cosmetic':
        price_of_finishing = "price_cosmetic"
        cac_age_of_repair(chat_id, user_id)
        cache_storage.set_value(f'price_of_finishing:{chat_id}', price_of_finishing)
    elif data == 'cac_price_good':
        price_of_finishing = "price_good"
        cac_age_of_repair(chat_id, user_id)
        cache_storage.set_value(f'price_of_finishing:{chat_id}', price_of_finishing)
    elif data == 'cac_price_perfect':
        price_of_finishing = "price_perfect"
        cac_age_of_repair(chat_id, user_id)
        cache_storage.set_value(f'price_of_finishing:{chat_id}', price_of_finishing)
    elif data == 'cac_price_design':
        price_of_finishing = "price_design"
        cac_age_of_repair(chat_id, user_id)
        cache_storage.set_value(f'price_of_finishing:{chat_id}', price_of_finishing)
    elif data == 'cac_back_to_cmrc':
        cac_minsk_region_choice(chat_id, user_id)
    elif data == 'cac_back_to_cmsc':
        cac_minsk_street_choice(chat_id, user_id)
    elif data == 'cac_back_to_chn':
        cac_house_number(chat_id, user_id)
    elif data == 'cac_back_to_ctoh':
        cac_type_of_house(call.message)
    elif data == 'cac_back_to_cr':
        cac_repair(call.message.chat.id)
    elif data == 'cac_back_to_caoh':
        cac_age_of_house(chat_id, user_id)
    elif data == 'cac_back_to_cnore':
        cac_number_of_rooms_entry(chat_id, user_id)
    elif data == 'cac_back_to_cta':
        cac_age_of_house(chat_id, user_id)
    elif data == 'cac_back_to_caor':
        cac_age_of_repair(chat_id, user_id) 
    elif data == 'r_property_appreciation':
        r_property_appreciation(call.message)
    elif data == "r_restart":
        r_restart(call.message)
    elif data == 'r_share' or data == 'r_1room' or data == 'r_2room' or data == 'r_3room' or data == 'r_4room' or data == 'r_5room':
        chat_id = call.message.chat.id
        cache_storage.set_value(f'r_num_of_rooms:{chat_id}', data)
        r_forecast_period(call.message.chat.id) 
    elif data == 'back_to_rpa':
        r_property_appreciation(call.message)
    elif data == 'back_to_raa':
        r_apartment_area(chat_id, user_id)
    elif data == 'back_to_rfp':
        r_forecast_period(chat_id, user_id)
    elif data == 'back_to_rrp':
        r_rental_price(chat_id, user_id)
    elif data == 'back_to_rmc':
        r_maintenance_cost(chat_id, user_id)
    elif data == 'back_to_rnor':
        r_number_of_rooms(chat_id, user_id)
    elif data == 'services_sell':
        info = 'sell'
        cache_storage.set_value(f'type_of_service:{chat_id}', info)
        services_sell(chat_id, user_id)
    elif data == 'services_buy':
        info = 'buy'
        cache_storage.set_value(f'type_of_service:{chat_id}', info)
        services_sell(chat_id, user_id)
    elif data == 'services_docs':
        info = 'docs'
        cache_storage.set_value(f'type_of_service:{chat_id}', info)
        services_sell(chat_id, user_id)
    elif data == 'services_sell_final':
        services_sell_final2(chat_id, user_id)