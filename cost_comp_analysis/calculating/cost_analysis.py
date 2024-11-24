from inspect import currentframe
from decimal import Decimal
from abc import ABC
from consts import Consts
from utils.utils import logger
from utils.data import Results, UserData

class CostAnalysisFunctions(ABC):
    def __init__(self, user_data:UserData) -> None:
        super().__init__()
        self.user_data = user_data


    def __type_panel_comp(self) -> None:
        match self.user_data.house_info2: 
            case 'hrush':
                self.cost_min_house_price = Consts.price_panel_hruzh[0]
                self.cost_max_house_price = Consts.price_panel_hruzh[1]
            case 'brezh':
                self.cost_min_house_price = Consts.price_panel_brezh[0]
                self.cost_max_house_price = Consts.price_panel_brezh[1]
            case 'standart':
                self.cost_min_house_price = Consts.price_panel_standart_project[0]
                self.cost_max_house_price = Consts.price_panel_standart_project[1]
            case 'upgrade':
                self.cost_min_house_price = Consts.price_panel_upgrade[0]
                self.cost_max_house_price = Consts.price_panel_upgrade[1]


    def __type_brick_comp(self) -> None:
        match self.user_data.house_info2:
            case 'stalin':
                self.cost_min_house_price = Consts.price_brick_stalin[0]
                self.cost_max_house_price = Consts.price_brick_stalin[1]
            case 'hrush':
                self.cost_min_house_price = Consts.price_brick_hruzh[0]
                self.cost_max_house_price = Consts.price_brick_hruzh[1]
            case 'brezh':
                self.cost_min_house_price = Consts.price_brick_brezh[0]
                self.cost_max_house_price = Consts.price_brick_brezh[1]
            case 'standart':
                self.cost_min_house_price = Consts.price_brick_standart[0]
                self.cost_max_house_price = Consts.price_brick_standart[1]
            case 'upgrade':
                self.cost_min_house_price = Consts.price_brick_upgrade[0]
                self.cost_max_house_price = Consts.price_brick_upgrade[1]


    def __type_monolith_comp(self) -> None:
        match self.user_data.house_info2:
            case'mon_brick':
                self.cost_min_house_price = Consts.price_monolith_brick[0]
                self.cost_max_house_price = Consts.price_monolith_brick[1]
            case 'mon_panel':
                self.cost_min_house_price = Consts.price_monolith_panel[0]
                self.cost_max_house_price = Consts.price_monolith_panel[1]
            case 'mon_block':
                self.cost_min_house_price = Consts.price_monolith_frame_and_block[0]
                self.cost_max_house_price = Consts.price_monolith_frame_and_block[1]


    def __type_of_finishing(self) -> None:
        match self.user_data.price_of_finishing:
            case 'price_finishing':
                self.min_cost_price_of_finishing = Consts.price_finishing_m2[0]
                self.max_cost_price_of_finishing = Consts.price_finishing_m2[1]
            case 'price_big_repair':
                self.min_cost_price_of_finishing = Consts.price_big_repair_m2[0]
                self.max_cost_price_of_finishing = Consts.price_big_repair_m2[1]
            case 'price_cosmetic':
                self.min_cost_price_of_finishing = Consts.price_cosmetic_m2[0]
                self.max_cost_price_of_finishing = Consts.price_cosmetic_m2[1]
            case 'price_good':
                self.min_cost_price_of_finishing = Consts.price_good_m2[0]
                self.max_cost_price_of_finishing = Consts.price_good_m2[1]
            case 'price_perfect':
                self.min_cost_price_of_finishing = Consts.price_perfect_m2[0]
                self.max_cost_price_of_finishing = Consts.price_perfect_m2[1]
            case 'price_design':
                self.min_cost_price_of_finishing = Consts.price_design_m2[0]
                self.max_cost_price_of_finishing = Consts.price_design_m2[1]


    def __get_type_house_deprec_coef(self) -> None:
        const = Decimal('0.4')
        match self.user_data.house_info1:
            case 'panel':
                self.__type_panel_comp()
                self.cost_house_depr_coef = (
                    self.user_data['cac_age'] / Consts.lifespan_panel
                )
                self.cost_house_depr_coef = min(self.cost_house_depr_coef, const)
            case 'brick':
                self.__type_brick_comp()
                self.cost_house_depr_coef = (
                    self.user_data['cac_age'] / Consts.lifespan_brick
                )
                self.cost_house_depr_coef = min(self.cost_house_depr_coef, const)
            case 'monolith':
                self.__type_monolith_comp()
                self.cost_house_depr_coef = (
                    self.user_data['cac_age'] / Consts.lifespan_monolith
                )
                self.cost_house_depr_coef = min(self.cost_house_depr_coef, const)


    def __get_region_kad_coef(self) -> None:
        match self.user_data.chosen_region_name:
            case 'Центральный район':
                self.cost_kad_price = Consts.kad_price_average_minsk * (Decimal('343') / Decimal('234'))
            case 'Фрунзенский район':
                self.cost_kad_price = Consts.kad_price_average_minsk * (Decimal('273') / Decimal('234'))
            case 'Советский район':
                self.cost_kad_price = Consts.kad_price_average_minsk * (Decimal('283') / Decimal('234'))
            case 'Первомайский район':
                self.cost_kad_price = Consts.kad_price_average_minsk * (Decimal('253') / Decimal('234'))
            case 'Партизанский район':
                self.cost_kad_price = Consts.kad_price_average_minsk * (Decimal('238') / Decimal('234'))
            case 'Заводской район':
                self.cost_kad_price = Consts.kad_price_average_minsk
            case 'Ленинский район':
                self.cost_kad_price = Consts.kad_price_average_minsk * (Decimal('254') / Decimal('234'))
            case 'Октябрьский район':
                self.cost_kad_price = Consts.kad_price_average_minsk * (Decimal('257') / Decimal('234'))
            case 'Московский район':
                self.cost_kad_price = Consts.kad_price_average_minsk * (Decimal('265') / Decimal('234'))


    def __get_min_max_data(self, cost:str) -> dict:
        match cost:
            case 'min':
                return {
                    'cost_house_price': self.cost_min_house_price,
                    'price_of_finishing': self.min_cost_price_of_finishing
                }
            case 'max':
                return {
                    'cost_house_price': self.cost_max_house_price,
                    'price_of_finishing': self.max_cost_price_of_finishing
                }


    def __calc_cost_price(self, cost:str) -> int:
        data = self.__get_min_max_data(cost)
        return (int(((data['cost_house_price'] - (data['cost_house_price'] *\
                self.cost_house_depr_coef)) + (data['price_of_finishing'] -\
                (data['price_of_finishing'] * self.user_data.repair_coef)) +\
                self.cost_kad_price) * self.user_data.area +\
                self.user_data.furniture_cost, 100)) / self.user_data.area

    def __calc_min_max_costs(self) -> dict:
        return {
            'min': self.__calc_cost_price('min'),
            'max': self.__calc_cost_price('max')
        }


    def cost_analysis(self) -> dict:
        try:
            self.__get_type_house_deprec_coef()
            self.__type_of_finishing()
            self.__get_region_kad_coef()
            results = self.__calc_min_max_costs()
            return self.__results_formatter(results)        
        except Exception as e:
            logger.error(f"\nError in {self.__class_.__name__} \
                {currentframe().f_code.co_name}: {e}", exc_info=True)
            return self.__results_formatter(exc=True)


    def __results_formatter(self, results:dict[str, int]=None, exc:bool=None) -> Results:
        return Results(
            min_flat_cost_price = None if exc else results['min'],
            max_flat_cost_price = None if exc else results['max'],
            av_flat_cost_price = None if exc else int((results['min'] + results['max']) / 2, 100)
        )