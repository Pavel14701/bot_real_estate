from fsm import cache_storage
from decimal import Decimal


class CalculatingRentProfitable:
    def __init__(self, chat_id:int|str, user_id:int|str):
        self.user_id, self.chat_id = user_id, chat_id
        self.num_of_rooms = str(cache_storage.get_value(user_id, chat_id, 'r_num_of_rooms'))
        self.forecast_period = Decimal(str(cache_storage.get_value(user_id, chat_id, 'r_forecast_period')))
        self.maintenance_costs = Decimal(str(cache_storage.get_value(user_id, chat_id, 'r_maintenance_costs')))
        self.rental_price = Decimal(str(cache_storage.get_value(user_id, chat_id, 'r_rental_price')))
        self.property_appreciation = Decimal(str(cache_storage.get_value(user_id, chat_id, 'r_property_appreciation')))
        self.discount_rate, self.inflation_rate = Decimal('0.054'), Decimal('0.03') 
        self.tax_rate, self.house_deprec = Decimal('0.87'), Decimal('0.00379')
        self.infl_maint_cost = Decimal('0')
        self.__get_vacancy_deprec()


    def __get_vacancy_deprec(self):
        if self.user_data['r_num_of_rooms'] == 'r_share':
            self.vacancy_rate = Decimal('0.77')
            self.house_deprec = Decimal('0.00395')
        elif self.user_data['r_num_of_rooms'] == 'r_1room':
            self.vacancy_rate = Decimal('0.89')
            self.house_deprec = Decimal('0.00380')
        elif self.user_data['r_num_of_rooms'] == 'r_2room':
            self.vacancy_rate = Decimal('0.84')
            self.house_deprec = Decimal('0.00375')      
        elif self.user_data['r_num_of_rooms'] == 'r_3room':
            self.vacancy_rate = Decimal('0.82')
            self.house_deprec = Decimal('0.00370')
        elif self.user_data['r_num_of_rooms'] == 'r_4room':
            self.vacancy_rate = Decimal('0.79')
            self.house_deprec = Decimal('0.00365')
        elif self.user_data['r_num_of_rooms'] == 'r_5room':
            self.vacancy_rate = Decimal('0.77')
            self.house_deprec = Decimal('0.00360')


    def __apartment_value(self):
        coef = self.__find_coef()
        for i in range(1, int(self.forecast_period)+1):
            self.infl_maint_cost += self.maintenance_costs * ((Decimal('1') + self.inflation_rate) ** Decimal(i))
        net_rental_income = self.rental_price * self.vacancy_rate * self.tax_rate * Decimal('12')
        r_cf = Decimal('0')
        for i in range(1, int(self.forecast_period)+1): 
            r_cf += net_rental_income / (Decimal('1') + self.discount_rate)**Decimal(i)
            pre_property_appreciation_up = self.property_appreciation * ((Decimal('1') + self.inflation_rate + coef) ** Decimal(i))
            pre_property_appreciation_down = self.property_appreciation * ((Decimal('1') + self.inflation_rate - coef) ** Decimal(i))
            self.future_apartment_value_up = pre_property_appreciation_up * (Decimal('1') - self.house_deprec) ** self.forecast_period
            self.future_apartment_value = self.property_appreciation * (Decimal('1') - self.house_deprec) ** self.forecast_period
            self.future_apartment_value_down = pre_property_appreciation_down * (Decimal('1') - self.house_deprec) ** self.forecast_period
            self.present_apartment_value_up = self.future_apartment_value_up + net_rental_income / ((Decimal('1') + self.discount_rate) ** self.forecast_period) - self.infl_maint_cost
            self.present_apartment_value = self.future_apartment_value + net_rental_income / ((Decimal('1') + self.discount_rate) ** self.forecast_period) - self.infl_maint_cost
            self.present_apartment_value_down = self.future_apartment_value_down + net_rental_income / ((Decimal('1') + self.discount_rate) ** self.forecast_period) - self.infl_maint_cost


    def __find_coef(self) -> Decimal:
        if self.num_of_rooms == 'r_share':
            return Decimal('0.0075')
        elif self.num_of_rooms == 'r_1room':
            return Decimal('0.0045')
        elif self.num_of_rooms == 'r_2room':
            return Decimal('0.0050')
        elif self.num_of_rooms == 'r_3room':
            return Decimal('0.0055')
        elif self.num_of_rooms == 'r_4room':
            return Decimal('0.0055')
        elif self.num_of_rooms == 'r_5room':
            return Decimal('0.0045')

    def __is_renting_profitable(self):
        self.profitable: bool = (self.present_apartment_value > self.property_appreciation)
        self.profitable_up: bool = (self.present_apartment_value_up > self.property_appreciation)
        self.profitable_down: bool = (self.present_apartment_value_down > self.property_appreciation)


    def rent_results(self):
        self.__apartment_value()
        self.__is_renting_profitable()
        cache_storage.set_value(self.user_id, self.chat_id, 'r_present_apartment_value_up', self.present_apartment_value_up)
        cache_storage.set_value(self.user_id, self.chat_id, 'r_present_apartment_value', self.present_apartment_value)
        cache_storage.set_value(self.user_id, self.chat_id, 'r_present_apartment_value_down', self.present_apartment_value_down)
        cache_storage.set_value(self.user_id, self.chat_id, 'r_market_apartment_price', self.property_appreciation)
        cache_storage.set_value(self.user_id, self.chat_id, 'r_is_profitable', self.profitable)
        cache_storage.set_value(self.user_id, self.chat_id, 'r_is_profitable_up', self.profitable_up)
        cache_storage.set_value(self.user_id, self.chat_id, 'r_is_profitable_down', self.profitable_down)