import os
from abc import ABC, abstractmethod
from telebot.types import Message, InlineKeyboardMarkup
from bot_instance import bot
from datasets.userdata import CacUserData
from cost_comp_analysis.calculating.cost_comp_functions import CostComparativeAnalysisFunctions
from utils.utils import del_msg, update_msg_to_del, send_image
from utils.data import UserData, Results


class ResultsSendler(ABC):
    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def send_greeting(self, chat_id:int|str, user_id:int|str) -> None:
        pass

    @abstractmethod
    def create_keyboard17(self) -> InlineKeyboardMarkup:
        pass

    def __results_keyboard(self, chat_id:int|str, to_del:list) -> list:
        return to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard17()))

    def __send_chart(self, chat_id:int|str, message:str, path:str) -> Message:
        msg = send_image(chat_id, path, message)
        os.remove(path)
        return msg


    def __result_exception_all(self, chat_id:int|str, user_id:int|str, to_del:list) -> None:
        to_del.append(
            bot.send_message(
                chat_id, 
                '😱Опаньки, похоже возникли проблемы.😱\n Если вы не пользовались \
                    функцией рассчёта раньше, то нужно ей воспользоваться, \n я не могу взять \
                    данные вашей о вашем объекте из воздуха. \n Пожалуйста, воспользуйтесь \
                    функцией рассчёта, \n с помощью кнопки начать. 😁', 
                parse_mode='Markdown'
            )
        )
        update_msg_to_del(chat_id, user_id, to_del)
        return self.send_greeting(chat_id, user_id)


    def __results_cost(self, chat_id:int|str, user_data:UserData, results:Results, to_del:list) -> list:
        return to_del.append(
            bot.send_message(
                chat_id, 
                f'** ЗАТРАТНЫЙ АНАЛИЗ СТОИМОСТИ ОБЪЕКТА ** \n\n Исходя из введённых вами данных, \
                    был произведён рассчёт стоимости вашего объекта. \n Рекомендуемый диапозон \
                    для продажи, без учёта данных сделок: \
                    {round(int(results.min_flat_cost_price*user_data.area), 100)} — \
                    {round(int(results.max_flat_cost_price*user_data.area), 100)}',
            parse_mode='Markdown'
            )
        )


    def __results_comp(self, chat_id:int, user_data:UserData, results:Results, to_del:list, flag:str, comp_list_regions:list, comp_list_streets:list) -> list:
        if flag == 'regions':
            return to_del.append(
                self.__send_chart(
                    chat_id,
                    f'** СРАВНИТЕЛЬНЫЙ АНАЛИЗ \n ДАННЫЕ СДЕЛОК, {user_data.chosen_region_name.upper()} \
                        **\n\n Цена, которая чаще всего встречается в выбранном районе($/м2): \
                        {results.av_flat_price} \n Минимальная зафиксированная цена, в выбранном \
                        районе($/м2): {results.comp_low_regions} \n Максимальная зафиксированная цена, в \
                        выбранном районе($/м2): {results.comp_high_regions} \n Рекомендуемый ценовой \
                        диапозон, без учёта данных сделок на вашей улице(общий прогноз): \
                        {round(int(results.comp_low_regions*user_data.area), 100)} — \
                        {round(int(results.comp_high_regions*user_data.area), 100)}',
                    path = f'.content/temp/region_minsk_{chat_id}.jpg'
                )
            )
        elif flag == 'streets':
            return to_del.append(
                self.__send_chart(
                    chat_id,
                    f'** СРАВНИТЕЛЬНЫЙ АНАЛИЗ \n ДАННЫЕ СДЕЛОК, {user_data.chosen_street_name.upper()} \
                        **\n\n Цена, которая чаще всего встречается на выбранной улице($/м2): \
                        {results.av_flat_price} \n Минимальная зафиксированная цена, на выбранной \
                        улице($/м2): {results.comp_low_streets} \n Максимальная зафиксированная цена, на \
                        выбранной улице($/м2): {results.comp_high_streets} \n Рекомендуемый ценовой диапозон, \
                        без учёта данных сделок района и ремонта(относительный прогноз): \
                        {round(int(results.comp_flat_min_streets*user_data.area), 100)} — \
                        {round(int(results.comp_high_streets*user_data.area), 100)}', 
                    path = f'.content/temp/street_{chat_id}.jpg'
                    )
                )


    def __results_all(self, chat_id:int|str, results:Results, to_del:list) -> list:
        return to_del.append(
            bot.send_message(
                chat_id,
                f'** ИТОГОВЫЙ АНАЛИЗ СТОИМОСТИ ОБЪЕКТА ** \n\n Исходя из всех вышеперечисленных \
                    анализов и введённых вами данных, был произведён рассчет максимально \
                    приемлемого диапазона, для продажи. \n Рекомендуемый ценовой диапазон \
                    для продажи вашего объекта: {results.min_flat_cost_price} — {results.max_flat_cost_price}\n\
                    ВНИМАНИЕ!!! Стоимость может изменяться из-за смены рыночной \
                    коньюктуры(как в вашу пользу, так и против вас)',
                parse_mode='Markdown'
            )
        )


    def __accuracy_warn(self, chat_id:int|str, user_data:UserData, to_del:list) -> list:
        return to_del.append(
            bot.send_message(
                chat_id,
                f"Ошибка, нет сделок на ул. {user_data.chosen_street_name.upper()} по \
                    заданным параметрам. \n Внимание, точность рассчёта снижена, рекомендуем \
                    проконсультироваться со специалистом.",
                parse_mode='Markdown'
            )
        )


    def calculate_results(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        try:
            to_del = []
            db = CacUserData()
            user_data = db.get_user_data_from_db(user_id)
            comp_list_regions = db.find_region_deals(user_data)
            comp_list_streets = db.find_street_deals(user_data)
            results = CostComparativeAnalysisFunctions(user_id, user_data, comp_list_regions, comp_list_streets).results()
            if results.av_flat_price == 0:
                self.__result_exception_all(chat_id, user_id, to_del)
            elif results.comp_high_regions == 0 and results.comp_low_regions == 0:
                self.__result_exception_all(chat_id, user_id, to_del)
            elif results.comp_flat_av_streets == 0 and results.comp_flat_max_streets == 0 and results.comp_flat_min_streets == 0:
                self.__results_without_streets(chat_id, user_data, user_data, results, to_del)
            else:
                self.__results(chat_id)
        except Exception as e:
            self.__result_exception_all(chat_id, user_id, to_del)


    def __results(self, chat_id:int|str, user_id:int|str, user_data:UserData, results:Results, to_del:list) -> list:
        # sourcery skip: class-extract-method
        to_del = self.__results_cost(chat_id, results, to_del)
        for flag in ['regions', 'streets']:
            to_del = self.__results_comp(chat_id, user_data, results, to_del, flag=flag)
        to_del = self.__results_all(self, chat_id, results, to_del)
        to_del =self.__results_keyboard(chat_id, to_del)
        update_msg_to_del(chat_id, user_id, to_del)


    def __results_without_streets(self, chat_id:int|str, user_id:int|str, user_data:UserData, results:Results, to_del:list) -> None:
        to_del = self.__results_cost(chat_id, results, to_del)
        to_del = self.__results_comp(self, chat_id, user_data, results, to_del, flag='regions')
        to_del = self.__accuracy_warn(chat_id, user_data, to_del)
        to_del = self.__results_all(self, chat_id, results, to_del)
        to_del =self.__results_keyboard(chat_id, to_del)
        update_msg_to_del(chat_id, user_id, to_del)