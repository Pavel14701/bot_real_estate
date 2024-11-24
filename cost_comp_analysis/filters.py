from telebot.types import CallbackQuery
from cost_comp_analysis.dialog import CostComparativeAnalysis
from fsm import cache_storage
from utils.utils import create_msg_thread


class CostCompCallbackFilter:
    def region_choice_callback_filter(self, call:CallbackQuery) -> str:
        valid_data = (
            'cac_centr', 'cac_frunz', 'cac_lenin',
            'cac_moscow', 'cac_zavod', 'cac_firstmay',
            'cac_october', 'cac_sovet', 'cac_partiz'
        )
        return call.data in valid_data

    def handle_keyboard_region_choice(self, call:CallbackQuery) -> None:
        chat_id, user_id = call.message.chat.id, call.from_user.id
        match call.data:
            case 'cac_centr':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Центральный район', 'chosen_region_name', 'Центральный район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_frunz':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Фрунзенский район', 'chosen_region_name', 'Фрунзенский район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_lenin':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Ленинский район', 'chosen_region_name', 'Ленинский район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_moscow':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Московский район', 'chosen_region_name', 'Московский район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_zavod':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Заводской район', 'chosen_region_name', 'Заводской район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_firstmay':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Первомайский район', 'chosen_region_name', 'Первомайский район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_october':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Октябрьский район', 'chosen_region_name', 'Октябрьский район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_sovet':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Советский район', 'chosen_region_name', 'Советский район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_partiz':
                create_msg_thread(chat_id, user_id, 'Вы выбрали Партизанский район', 'chosen_region_name', 'Партизанский район')
                return CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)

    def cost_comp_callback_filter(self, call:CallbackQuery) -> str:
        valid_data = (
            'cac_centr', 'cac_frunz', 'cac_lenin',
            'cac_moscow', 'cac_zavod', 'cac_firstmay',
            'cac_october', 'cac_sovet', 'cac_partiz'
        )
        return call.data in valid_data

    def handle_keyboard_house_type(self, call:CallbackQuery) -> None:
        chat_id, user_id = call.message.chat.id, call.from_user.id
        data:str = call.data
        match data:
            case 'cac_restart':
                create_msg_thread(chat_id, user_id, 'Перезапуск функции оценки')
                return CostComparativeAnalysis().send_greeting(chat_id, user_id)
            case 'cac_calculate_results':
                return CostComparativeAnalysis().calculate_results(chat_id, user_id)
            case 'cac_minsk_region_entry':
                return CostComparativeAnalysis().minsk_region_choice(chat_id, user_id)
            case data.startswith('street_'):
                chosen_street_name = data[7:]
                create_msg_thread(chat_id, user_id, f'Вы выбрали вариант: {chosen_street_name}', 'chosen_street_name', chosen_street_name)
                return CostComparativeAnalysis().house_number(chat_id, user_id)

    def house_mat_callback_filter(self, call:CallbackQuery) -> str:
        valid_data = ('cac_panel', 'cac_monolith', 'cac_brick')
        return call.data in valid_data

    def handle_keyboard_house_mat(self, call:CallbackQuery) -> None:
        chat_id, user_id = call.message.chat.id, call.from_user.id
        match call.data:
            case 'cac_panel':
                create_msg_thread(chat_id, user_id, 'Вы выбрали панельный тип дома.', 'house_info1', 'panel')
                return CostComparativeAnalysis().type_panel(chat_id, user_id)
            case 'cac_monolith':
                create_msg_thread(chat_id, user_id, 'Вы выбрали монолитный тип дома.', 'house_info1', 'monolith')
                return CostComparativeAnalysis().type_monolith(chat_id, user_id)
            case 'cac_brick':
                create_msg_thread(chat_id, user_id, 'Вы выбрали кирпичный тип дома.', 'house_info1', 'brick')
                return CostComparativeAnalysis().type_brick(chat_id, user_id)

    def house_type_callback_filter(self, call:CallbackQuery) -> str:
        valid_data = (
            'cac_hrush', 'cac_brezh', 'cac_standart',
            'cac_upgrade', 'cac_stalin', 'cac_mon_panel',
            'cac_mon_brick', 'cac_mon_block'
            )
        return call.data in valid_data

    def handle_keyboard_house_type(self, call:CallbackQuery) -> None:
        chat_id, user_id = call.message.chat.id, call.from_user.id
        match call.data:
            case 'cac_hrush':
                create_msg_thread(chat_id, user_id, 'Вы выбрали проект типа \"хрущёвка\".', 'house_info2', 'hrush')
                return CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_brezh':
                create_msg_thread(chat_id, user_id, 'Вы выбрали проект типа \"брежневка\".', 'house_info2', 'brezh')
                return CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_standart':
                create_msg_thread(chat_id, user_id, 'Вы выбрали стандартный тип проекта.', 'house_info2', 'standart')
                return CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_upgrade':
                create_msg_thread(chat_id, user_id, 'Вы выбрали улучшенный тип проекта.', 'house_info2', 'upgrade')
                return CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_stalin':
                create_msg_thread(chat_id, user_id, 'Вы выбрали проект типа \"Сталинка\".', 'house_info2', 'stalin')
                return CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_mon_panel':
                create_msg_thread(chat_id, user_id, 'Вы выбрали монолитно-панельный тип дома.', 'house_info2', 'mon_panel')
                return CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_mon_brick':
                create_msg_thread(chat_id, user_id, 'Вы выбрали каркасно-кирпичный тип дома.', 'house_info2', 'mon_brick')
                return CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_mon_block':
                create_msg_thread(chat_id, user_id, 'Вы выбрали каркасно-блочный тип дома.', 'house_info2', 'mon_block')
                return CostComparativeAnalysis().age_of_house(chat_id, user_id)

    def number_rooms_callback_filter(self, call:CallbackQuery) -> str:
        valid_data = (
            'cac_share', 'cac_1room', 'cac_2room',
            'cac_3room', 'cac_4room', 'cac_5room'
            )
        return call.data in valid_data

    def handle_keyboard_number_rooms(self, call:CallbackQuery) -> None:
        chat_id, user_id = call.message.chat.id, call.from_user.id
        match call.data:
            case 'cac_share':
                create_msg_thread(chat_id, user_id, 'Вы выбрали вариант: доля.', 'number_of_rooms', 0)
                return CostComparativeAnalysis().total_area(chat_id, user_id)
            case 'cac_1room':
                create_msg_thread(chat_id, user_id, 'Вы выбрали вариант: 1-комн.', 'number_of_rooms', 1)
                return CostComparativeAnalysis().total_area(chat_id, user_id)
            case 'cac_2room':
                create_msg_thread(chat_id, user_id, 'Вы выбрали вариант: 2-комн.', 'number_of_rooms', 2)
                return CostComparativeAnalysis().total_area(chat_id, user_id)
            case 'cac_3room':
                create_msg_thread(chat_id, user_id, 'Вы выбрали вариант: 3-комн.', 'number_of_rooms', 3)
                return CostComparativeAnalysis().total_area(chat_id, user_id)
            case 'cac_4room':
                create_msg_thread(chat_id, user_id, 'Вы выбрали вариант: 4-комн.', 'number_of_rooms', 4)
                return CostComparativeAnalysis().total_area(chat_id, user_id)
            case 'cac_5room':
                create_msg_thread(chat_id, user_id, 'Вы выбрали вариант: 5-комн.+', 'number_of_rooms', 5)
                return CostComparativeAnalysis().total_area(chat_id, user_id)

    def price_finishing_callback_filter(self, call:CallbackQuery) -> str:
        valid_data = (
            'cac_price_finishing', 'cac_price_big_repair', 'cac_price_cosmetic',
            'cac_price_good', 'cac_price_perfect', 'cac_price_design'
            )
        return call.data in valid_data

    def handle_keyboard_price_finishing(self, call:CallbackQuery) -> None:
        chat_id, user_id = call.message.chat.id, call.from_user.id
        match call.data:
            case 'cac_price_finishing':
                cache_storage.set_value(user_id, chat_id, 'price_of_finishing', 'price_of_finishing')
                return CostComparativeAnalysis().age_of_repair(chat_id, user_id)
            case 'cac_price_big_repair':
                cache_storage.set_value(user_id, chat_id, 'price_of_finishing', 'price_big_repair')
                return CostComparativeAnalysis().age_of_repair(chat_id, user_id)
            case 'cac_price_cosmetic':
                cache_storage.set_value(user_id, chat_id, 'price_of_finishing', 'price_cosmetic')
                return CostComparativeAnalysis().age_of_repair(chat_id, user_id)
            case 'cac_price_good':
                cache_storage.set_value(user_id, chat_id, 'price_of_finishing', 'price_good')
                return CostComparativeAnalysis().age_of_repair(chat_id, user_id)
            case 'cac_price_perfect':
                cache_storage.set_value(user_id, chat_id, 'price_of_finishing', 'price_perfect')
                return CostComparativeAnalysis().age_of_repair(chat_id, user_id)
            case 'cac_price_design':
                cache_storage.set_value(user_id, chat_id, 'price_of_finishing', 'price_design')
                return CostComparativeAnalysis().age_of_repair(chat_id, user_id)

    def cac_back_callback_filter(self, call:CallbackQuery) -> str:
        valid_data = (
            'cac_back_to_cmrc', 'cac_back_to_cmsc', 'cac_back_to_chn',
            'cac_back_to_ctoh', 'cac_back_to_cr', 'cac_back_to_caoh',
            'cac_back_to_cnore', 'cac_back_to_cta', 'cac_back_to_caor'
            )
        return call.data in valid_data

    def handle_keyboard_price_finishing(self, call:CallbackQuery) -> None:
        chat_id, user_id = call.message.chat.id, call.from_user.id
        match call.data:
            case 'cac_back_to_cmrc':
                CostComparativeAnalysis().minsk_region_choice(chat_id, user_id)
            case 'cac_back_to_cmsc':
                CostComparativeAnalysis().minsk_street_choice(chat_id, user_id)
            case 'cac_back_to_chn':
                CostComparativeAnalysis().house_number(chat_id, user_id)
            case 'cac_back_to_ctoh':
                CostComparativeAnalysis().type_of_house(call.message)
            case 'cac_back_to_cr':
                CostComparativeAnalysis().repair(call.message.chat.id)
            case 'cac_back_to_caoh':
                CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_back_to_cnore':
                CostComparativeAnalysis().number_of_rooms_entry(chat_id, user_id)
            case 'cac_back_to_cta':
                CostComparativeAnalysis().age_of_house(chat_id, user_id)
            case 'cac_back_to_caor':
                CostComparativeAnalysis().age_of_repair(chat_id, user_id)