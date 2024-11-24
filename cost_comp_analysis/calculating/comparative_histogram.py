from abc import ABC
from inspect import currentframe
import numpy as np, matplotlib.pyplot as plt
from utils.utils import logger
from utils.data import CostCompDataClass


class ComparativeHistogram(CostCompDataClass, ABC):
    def __init__(self, user_id:int, user_data:dict) -> None:
        CostCompDataClass.__init__(self)
        ABC.__init__(self)
        self.user_id = user_id
        self.user_data = user_data


    def create_histogram(self) -> str:
        try:
            bounds = self.__get_bounds()
            left = self.values[self.values < bounds['left_bound']]
            middle = self.values[(bounds['left_bound'] <= self.values) & (self.values < bounds['middle_bound'])]
            right = self.values[self.values >= bounds['middle_bound']]
            fig, ax = plt.subplots()
            n, bins, patches = ax.hist(self.values, bins=100, edgecolor='black', color='white')
            colors_dict = {(-np.inf, bounds['left_bound']): 'red',
                        (bounds['left_bound'], bounds['middle_bound']): '#DAB71A',
                        (bounds['middle_bound'], bounds['right_bound']): 'green'}
            alphas = [0.65, 0.6, 0.75]
            for i, patch in enumerate(patches):
                color = 'white'
                alpha = 1
                for j, ((low, high), c) in enumerate(colors_dict.items()):
                    if low <= bins[i] < high:
                        color = c
                        alpha = alphas[j]
                        break
                patch.set_facecolor(color)
                patch.set_alpha(alpha)
            self.__get_legend(self.regions, alphas)
            if self.regions: 
                path = f'./content/temp/region_minsk_{self.user_id}.jpg'
                plt.savefig(path)
                return path
            path = f'./content/temp/street_{self.user_id}.jpg'
            plt.savefig(path)
            return path
        except Exception as e:
            logger.error(f"\nError in {self.__class_.__name__} \
                {currentframe().f_code.co_name}: {e}", exc_info=True)


    def __get_legend(self, alphas:list[float]) -> None:
        try:
            plt.xlabel('Цена м²')
            plt.ylabel('Количество проданных')
            if self.regions:
                match self.user_data['number_of_rooms']:
                    case 0:
                        plt.title(' Все районы, Доля')
                    case _ :
                        plt.title(f'{self.user_data['chosen_region_name']},\
                            {self.user_data['number_of_rooms']} комн.')
            else:
                match self.user_data['number_of_rooms']:
                    case 0:
                        plt.title(f'{self.user_data['chosen_street_name']}, Доля')
                    case _ :
                        plt.title(f'{self.user_data['chosen_street_name']}, \
                            {self.user_data['number_of_rooms']} комн.')
            colors = ['red', '#DAB71A', 'green']
            labels = ['Низкая рыночная стоимость', 'Средняя стоимость', 'Высокая рыночная стоимость']
            handles = [plt.Rectangle((0,0),1,1, color=c, alpha=a) for c, a in zip(colors, alphas)]
            plt.legend(handles, labels, loc='upper right')
        except Exception as e:
            logger.error(f"Error in {self.__class_.__name__} \
                {currentframe().f_code.co_name}: {e}", exc_info=True)

    def __get_bounds(self) -> dict:
        try:
            match self.user_data['number_of_rooms']: 
                case 0:
                    return {
                        'left_bound': np.quantile(self.values, 0.184),
                        'middle_bound': np.quantile(self.values, 0.348),
                        'right_bound': np.quantile(self.values, 1)
                    }
                case 1:
                    return {
                        'left_bound': np.quantile(self.values, 0.34),
                        'middle_bound': np.quantile(self.values, 0.58),
                        'right_bound': np.quantile(self.values, 1)
                    }
                case 2:
                    return {
                        'left_bound': np.quantile(self.values, 0.28),
                        'middle_bound': np.quantile(self.values, 0.47),
                        'right_bound': np.quantile(self.values, 1)
                    }
                case 3:
                    return {
                        'left_bound': np.quantile(self.values, 0.37),
                        'middle_bound': np.quantile(self.values, 0.61),
                        'right_bound': np.quantile(self.values, 1)
                    }
                case 4:
                    return {
                        'left_bound': np.quantile(self.values, 0.239),
                        'middle_bound': np.quantile(self.values, 0.49),
                        'right_bound': np.quantile(self.values, 1)
                    }
                case 5:
                    return {
                        'left_bound': np.quantile(self.values, 0.22),
                        'middle_bound': np.quantile(self.values, 0.47),
                        'right_bound': np.quantile(self.values, 1)
                    }
        except Exception as e:
            logger.error(f"Error in {self.__class_.__name__} \
                {currentframe().f_code.co_name}: {e}", exc_info=True)