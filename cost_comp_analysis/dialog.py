import time
from decimal import Decimal
from datetime import datetime
from telebot.states.sync.context import StateContext
from telebot.types import Message, InputMediaPhoto
from bot_instance import bot
from fsm import cache_storage, UserStates
from utils.utils import del_msg, update_msg_to_del, create_thread, run_in_thread
from datasets.streetname import StreetName
from datasets.userdata import CacUserData
from cost_comp_analysis.results import ResultsSendler
from cost_comp_analysis.types import CostComparativeAnalysisMarkups
from utils.middlewares import LogExceptionMiddlewareMeta
from main_types import MainTypes

class CostComparativeAnalysis(MainTypes, CostComparativeAnalysisMarkups, ResultsSendler, meta_class=LogExceptionMiddlewareMeta):
    def __init__(self) -> None:
        MainTypes.__init__(self)
        CostComparativeAnalysisMarkups.__init__(self)
        ResultsSendler.__init__(self)


    def send_greeting(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        to_del = [bot.send_message(chat_id, 'Так, вы хотите узнать рыночную стоимость квартиры. Учтите, что я могу рассчитать только примерный диапазон,\n для точной оценки свяжитесь с нашим специалистом. Это бесплатно. Для рассчёёта мне нужно задать вам несколько вопросов, а потом покажу вам результаты. Вы не против ?\n Кстати, я запомню все ваши ответы и смогу в будущем рассчитать стоимость, потому что они не стоят на месте, а постоянно меняются.')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard1()))
        update_msg_to_del(chat_id, user_id, to_del)


    def minsk_region_choice(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        with open('./content/calc_cac/region.jpg', 'rb') as img:
            to_del = [bot.send_photo(chat_id, img, caption='Укажите район Минска, в котором расположен\
                оцениваемый объект.')]
        to_del.append (bot.send_message(chat_id, 'Выберите из списка', reply_markup=self.create_keyboard2()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_started')


    def minsk_street_choice(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.result_street_choice)
        with open('./content/calc_cac/street_choice.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Введите улицу, на которой находится\
                оцениваемый объект.')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard3()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    @bot.message_handler(state=UserStates.result_street_choice)
    def register_street_choice(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        if not (street_list := StreetName().street_names(message.text)):
            return self.street_choice_error(chat_id, user_id, message)
        with open('./content/calc_cac/bd.jpg', 'rb') as img1:
            to_del = [bot.send_photo(message.chat.id, img1, caption=f'Вы ввели {message.text}.\
                    По результатам сравнения с базой данных нашлось {len(street_list)} совпадений.')]
        to_del.append(bot.send_message(message.chat.id, 'Выберите улицу из списка:', reply_markup=self.create_keyboard4(street_list)))
        update_msg_to_del(chat_id, user_id, to_del)


    @run_in_thread()
    def street_choice_error(self, chat_id:int|str, user_id:int|str, message:Message) -> None:
        del_msg(chat_id, user_id)
        with open('./content/calc_cac/no_bd.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption=f'К сожалению, я не нашел улицу с названием\
                {message.text} в базе даннных.')]
        to_del.append(bot.send_message(chat_id, 'Пожалуйста, повторите ввод или свяжитесь со специалистом.'))
        update_msg_to_del(chat_id, user_id, to_del)
        time.sleep(3)
        return self.minsk_street_choice(chat_id, user_id, StateContext(message, bot))


    def house_number(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_for_type_of_house)
        with open('./content/calc_cac/numb_h.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Введите номер дома')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard5()))
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')
        update_msg_to_del(chat_id, user_id, to_del)


    @bot.message_handler(state=UserStates.waiting_for_type_of_house)
    def type_of_house(self, message: Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        with open('./content/calc_cac/panel.jpg', 'rb') as img1, \
            open('./content/calc_cac/brick.jpg', 'rb') as img2, \
            open('./content/calc_cac/mon.jpg', 'rb') as img3:
            to_del = [bot.send_photo(chat_id, img1, caption='Панельные дома — здания из железобетонных панелей, собранных на месте. Внешние стены — многослойные, с утеплителем; внутренние — однослойные. Различаются по размеру и материалам.')]
            to_del.append(bot.send_photo(chat_id, img2, caption='Кирпичный дом — это здание, построенное из кирпича, материала с высокой прочностью и долговечностью. Стены могут быть полнотелыми или пустотелыми, с различными отделочными вариантами. Кирпичные дома ценятся за их теплоизоляцию и эстетику.'))
            to_del.append(bot.send_photo(chat_id, img3, caption='Монолитный дом — это здание с бесшовным каркасом, отлитым из бетона поэтажно. Отсутствие стыков делает его прочным и устойчивым к погодным условиям.'))
        to_del.append(bot.send_message(chat_id, 'Выберите тип дома из списка'))
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard6()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    def send_media_in_group(self, chat_id:int, caption:str, paths:tuple[str]) -> list[Message]:
        media_list=[]
        for path in paths:
            with open(path, 'rb') as img:
                media_list.append(InputMediaPhoto(img), caption=caption)
        return bot.send_media_group(chat_id, media_list)


    def type_panel(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        paths = ('./content/calc_cac/panel/chruzh1.jpg', './content/calc_cac/panel/chruzh2.jpg')
        caption = "Хрущёвки — это типовые многоквартирные дома, которые были массово построены в СССР с\
            1956 по 1974 год. Они получили своё название в честь Никиты Хрущёва, который инициировал их \
                строительство как решение проблемы нехватки жилья после Второй мировой войны. \
                    Хрущёвки обычно имеют 4-5 этажей, хотя встречаются и 2-3, а также 8-9 \
                        этажные варианты. Эти дома отличаются простой и функциональной архитектурой, \
                            а квартиры в них имеют относительно небольшие размеры"
        to_del = self.send_media_in_group(chat_id, caption, paths)
        paths = ('./content/calc_cac/panel/brezh1.jpg', './content/calc_cac/panel/brezh2.jpg')
        caption = "Брежневки — это типовые жилые дома, которые строились в СССР с 1964 по 1985 год. Они \
            названы в честь Леонида Брежнева и являются улучшенной версией хрущёвок. Брежневки представляют\
                собой панельные, блочные или кирпичные дома, которые отличаются более продуманной \
                    планировкой и большей площадью квартир. В отличие от хрущёвок, в брежневках иногда \
                        есть лифты, присутствуют балконы или лоджии, а также улучшенная звуко и \
                            теплоизоляция."
        to_del.extend(self.send_media_in_group(chat_id, caption, paths))
        paths = ('./content/calc_cac/panel/standart1.jpg', './content/calc_cac/panel/standart2.jpg')
        caption = "Дома стандартного проекта в Минске и других городах бывшего СССР — это многоэтажные \
            здания, в основном из железобетонных панелей, хотя встречаются и кирпичные варианты. Типичные \
                дома имеют от 5 до 12 этажей, с преобладанием 9-этажных конструкций. Квартиры разнообразны \
                    по размеру и могут включать от 1 до 4 комнат, оборудованы встроенными шкафами и \
                        мусоропроводами. Стандартная высота потолков составляет 2,5 метра. В большинстве \
                            домов установлены лифты, а на первых этажах расположены магазины и другие \
                                объекты инфраструктуры."
        to_del.extend(self.send_media_in_group(chat_id, caption, paths))
        paths = ('./content/calc_cac/panel/upgrade1.jpg', './content/calc_cac/panel/upgrade2.jpg')
        caption = "Дома с улучшенными планировками — это современные жилые здания с повышенным комфортом и \
            энергоэффективностью. Они отличаются качественными материалами, улучшенной тепло- и \
                звукоизоляцией, разнообразной планировкой, большими площадями и эстетичными фасадами. \
                    Высота потолков 2.5 - 2.7 метра."
        to_del.extend(self.send_media_in_group(chat_id, caption, paths))
        to_del.append(bot.send_message(chat_id, 'Существует несколько видов панельных домов.\
            Выберите к какому из перечисленных видов относится ваш.',
            reply_markup=self.create_keyboard7()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    def type_brick(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        paths = ('./content/calc_cac/brick/stalin1.jpg', './content/calc_cac/brick/stalin2.jpg')
        caption="“Сталинки” — это название, данное многоквартирным домам, построенным в СССР с конца 1930-х до середины 1950-х годов, в основном в период правления Иосифа Сталина. Эти здания отличаются капитальным строением, высокими потолками, просторными квартирами и часто выполнены в стиле неоклассицизма. Высокие потолки 2.7 - 3 метра. Сталинки известны своей прочностью, качественными материалами и декоративными элементами, такими как лепнина на фасадах"
        to_del = self.send_media_in_group(chat_id, caption, paths)
        paths = ('./content/calc_cac/brick/chruzh1.jpg', './content/calc_cac/brick/chruzh2.jpg')
        caption="Хрущёвки — это типовые многоквартирные дома, которые были массово построены в СССР с 1956 по 1974 год. Они получили своё название в честь Никиты Хрущёва, который инициировал их строительство как решение проблемы нехватки жилья после Второй мировой войны. Хрущёвки обычно имеют 4-5 этажей, хотя встречаются и 2-3, а также 8-9 этажные варианты. Эти дома отличаются простой и функциональной архитектурой, а квартиры в них имеют относительно небольшие размеры"
        to_del.extend(self.send_media_in_group(chat_id, caption, paths))
        paths = ('./content/calc_cac/brick/brezh1.jpg', './content/calc_cac/brick/brezh2.jpg')
        caption="Брежневки — это типовые жилые дома, которые строились в СССР с 1964 по 1985 год. Они названы в честь Леонида Брежнева и являются улучшенной версией хрущёвок. Брежневки представляют собой панельные, блочные или кирпичные дома, которые отличаются более продуманной планировкой и большей площадью квартир. В отличие от хрущёвок, в брежневках часто есть лифты, балконы или лоджии, а также улучшенная звукоизоляция"
        to_del.extend(self.send_media_in_group(chat_id, caption, paths))
        paths = ('./content/calc_cac/brick/standart1.jpg', './content/calc_cac/brick/standart2.jpg')
        caption="Дома стандартного проекта в Минске и других городах бывшего СССР — это многоэтажные здания, в основном из железобетонных панелей, хотя встречаются и кирпичные варианты. Типичные дома имеют от 5 до 12 этажей, с преобладанием 9-этажных конструкций. Квартиры разнообразны по размеру и могут включать от 1 до 4 комнат, оборудованы встроенными шкафами и мусоропроводами. Стандартная высота потолков составляет 2,5 метра. В большинстве домов установлены лифты, а на первых этажах расположены магазины и другие объекты инфраструктуры."
        to_del.extend(self.send_media_in_group(chat_id, caption, paths))
        paths = ('./content/calc_cac/brick/upgrade1.jpg', './content/calc_cac/brick/upgrade2.jpg')
        caption="Дома с улучшенными планировками — это современные жилые здания с повышенным комфортом и энергоэффективностью. Они отличаются качественными материалами, улучшенной тепло- и звукоизоляцией, разнообразной планировкой, большими площадями и эстетичными фасадами. Высота потолков 2.5 - 2.7 метра."
        to_del.extend(self.send_media_in_group(chat_id, caption, paths))
        to_del.append(bot.send_message(chat_id, 'Существует несколько видов панельных домов. \
            Выберите к какому из перечисленных видов относится ваш.',
            reply_markup=self.create_keyboard8()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    def type_monolith(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        paths = ('./content/calc_cac/monolith/mon_brick1.jpg', './content/calc_cac/monolith/mon_brick2.jpg')
        caption="Монолитно-кирпичные многоквартирные дома — это сочетание монолитного железобетонного каркаса для прочности и устойчивости с кирпичной кладкой для отличной тепло- и звукоизоляции. Эти дома позволяют гибкую планировку пространства, включая свободные планировки и большие окна, обеспечивая комфортное проживание. Высокая долговечность, до 150 лет, и возможность реализации разнообразных архитектурных стилей делают их популярным выбором для строительства. Важной особенностью является повышенная энергоэффективность, снижающая эксплуатационные расходы."
        to_del = self.send_media_in_group(chat_id, caption, paths)
        paths = ('./content/calc_cac/monolith/mon_block1.jpg', './content/calc_cac/monolith/mon_block2.jpg')
        caption="Каркасно-блочные дома - это тип строений, где основу конструкции составляет монолитный железобетонный каркас, а стены дополнительно утепляются и закрываются блоками. Такая технология строительства позволяет создавать прочные и долговечные здания, обладающие хорошей тепло- и звукоизоляцией. Монолитный каркас отливается из бетонной массы, что обеспечивает единую бесшовную конструкцию, устойчивую к погодным явлениям и сейсмической активности. Высокие потолки, свободные планировки. Блоки, используемые для стен, могут быть изготовлены из различных материалов, таких как пеноблоки или газобетон, что добавляет дополнительные изоляционные свойства добавь характеристики планировок"
        to_del.extend(self.send_media_in_group(chat_id, caption, paths))
        to_del.append(bot.send_message(chat_id, 'Существует несколько видов панельных домов. Выберите к \
            какому из перечисленных видов относится ваш.',
            reply_markup=self.create_keyboard9()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_state', 'cac_in_progress')


    def age_of_house(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_age_of_house)
        with open('./content/calc_cac/age_of_house.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Введите год постройки дома')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard10()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    @bot.message_handler(state = UserStates.waiting_age_of_house)
    @run_in_thread
    def cac_age_of_house_handler(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        try:
            year = int(message.text)
        except ValueError:
            to_del = bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или свяжитесь со специалистом')
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            return self.age_of_house(chat_id, user_id, StateContext(message, bot))
        current_year = datetime.now().year
        if year >= 1900 and year <= current_year:
            to_del = bot.send_message(chat_id, f'Вы ввели {year} год. Возраст дома составляет {current_year - year} года(лет).')
            cac_age = current_year - year
            update_msg_to_del(chat_id, user_id, to_del)
            cache_storage.set_value(user_id, chat_id, 'cac_age', cac_age)
            time.sleep(2)
            return self.number_of_rooms_entry(chat_id, user_id)
        else:
            to_del = bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или обратитесь  к специалисту')
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            return self.age_of_house(chat_id, user_id, StateContext(message, bot))


    def number_of_rooms_entry(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        with open('./content/calc_cac/rooms.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Сколько комнат в квартире?')]
        to_del.append(bot.send_message(chat_id, 'Выберите вариант из списка:', reply_markup=self.create_keyboard11()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    def total_area(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_area_of_house)
        with open('./content/calc_cac/area.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Введите общую площадь квартиры')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard12()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    @bot.message_handler(state = UserStates.waiting_area_of_house)
    @run_in_thread
    def total_area_handler(self, message:Message):
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        try:
            area = round(Decimal(message.text.replace(",", ".")), 2)
            if area >= Decimal('1') and area <= Decimal('999'):
                to_del = bot.send_message(chat_id, f'Вы ввели {area} м².')
                cache_storage.set_value(user_id, chat_id, 'area', area)
                update_msg_to_del(chat_id, user_id, to_del)
                time.sleep(2)
                return self.repair(chat_id, user_id)
            else:
                to_del = bot.send_message(chat_id, 'Ошибка, максимальный диапозон 1-999 м² пожалуйста повторите ввод или обратитесь  к специалисту')
                update_msg_to_del(chat_id, user_id, to_del)
                time.sleep(2)
                return self.total_area(chat_id, user_id)
        except ValueError:
            to_del = bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или обратитесь  к специалисту')
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            return self.total_area(chat_id, user_id)


    def repair(self, chat_id:int|str, user_id:int|str) -> None:
        del_msg(chat_id, user_id)
        paths = ('./content/calc_cac/remont/chern.jpg', './content/calc_cac/remont/need_rem.jpg', 
            './content/calc_cac/remont/cosmetic.jpg', './content/calc_cac/remont/good.jpg',
            './content/calc_cac/remont/design.jpg'
        )
        caption="Выберите тип ремонта из списка\n\n \
            Черновая \n\n \
            Нуждается в ремонте \n\n \
            Только косметика \n\n \
            Хороший \n\n \
            Отличный \n\n \
            Дизайнерский"
        to_del = self.send_media_in_group(chat_id, caption, paths)
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard13()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    def age_of_repair(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_age_of_repair)
        with open('./content/calc_cac/age_of_repair.jpg', 'rb') as img1:
            to_del = [bot.send_photo(chat_id, img1, caption='Введите возраст ремонта, в годах')]
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard14()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    @bot.message_handler(state = UserStates.waiting_age_of_repair)
    @run_in_thread
    def cac_age_of_repair_handler(self, message:Message) -> None:
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        try:
            age_repair = int(message.text)
        except ValueError:
            to_del = bot.send_message(chat_id, 'Ошибка, не верный формат. Пожалуйста повторите ввод или свяжитесь со специалистом')
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            return self.age_of_repair(chat_id, user_id, StateContext(message, bot))
        if age_repair < 0:
            to_del = bot.send_message(chat_id, 'Ошибка, число не должно быть отрицательным. Пожалуйста повторите ввод или свяжитесь со специалистом')
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            return self.age_of_repair(chat_id, user_id, StateContext(message, bot))
        if age_repair > 10:
            repair_coef = Decimal('0.3')
            to_del = bot.send_message(chat_id, f'Вы ввели {age_repair} года(лет).')
            cache_storage.set_value(f'cac_repair_coef:{chat_id}', repair_coef)
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            self.price_furniture(chat_id, user_id, StateContext(message, bot))
        else:
            cac_repair_coef = Decimal('0.01') + Decimal('0.03') * age_repair
            bot.send_message(chat_id, f'Вы ввели {age_repair} года(лет).')
            cache_storage.set_value(user_id, chat_id, 'cac_repair_coef', cac_repair_coef)
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            return self.price_furniture(chat_id, user_id, StateContext(message, bot))


    def price_furniture(self, chat_id:int|str, user_id:int|str, state:StateContext) -> None:
        del_msg(chat_id, user_id)
        state.set(UserStates.waiting_price_of_furniture)
        paths = ('./content/calc_cac/furniture/kitchen.jpg', './content/calc_cac/furniture/bathroom.jpg',
            './content/calc_cac/furniture/tv.jpg')
        caption="Введите стоимость мебели и техники, которую вы планируете оставить."
        to_del = self.send_media_in_group(chat_id, caption, paths)
        to_del.append(bot.send_message(chat_id, 'Меню', reply_markup=self.create_keyboard15()))
        update_msg_to_del(chat_id, user_id, to_del)
        cache_storage.set_value(user_id, chat_id, 'reminder_states', 'cac_in_progress')


    @bot.message_handler(state = UserStates.waiting_price_of_furniture)
    @run_in_thread
    def cac_price_furniture_handler(self, message:Message):
        # sourcery skip: remove-unnecessary-cast
        chat_id, user_id = message.chat.id, message.from_user.id
        del_msg(chat_id, user_id)
        try:
            furniture_price = int(message.text)
        except ValueError:
            to_del = bot.send_message(chat_id, 'Ошибка, пожалуйста повторите ввод или свяжитесь со специалистом')
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            return self.price_furniture(chat_id, user_id)
        if furniture_price < 0:
            to_del = bot.send_message(chat_id, 'Ошибка, число не должно быть отрицательным. Пожалуйста повторите ввод или свяжитесь со специалистом')
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            return self.price_furniture(chat_id, user_id)
        else:
            cache_storage.set_value(user_id, chat_id, 'furniture_cost', Decimal(furniture_price))
            user_data = cache_storage.get_values(user_id, chat_id)
            to_del = bot.send_message(chat_id, f'Вы ввели {int(furniture_price)}')
            update_msg_to_del(chat_id, user_id, to_del)
            time.sleep(2)
            create_thread(target=CacUserData().add_user_data_to_database, args=(user_id, user_data), daemon=True)
            return self.calculate_results(chat_id, user_id)