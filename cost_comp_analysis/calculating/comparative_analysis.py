import math, numpy as np
from decimal import Decimal
from inspect import currentframe
from abc import ABC
from cost_comp_analysis.calculating.comparative_histogram import ComparativeHistogram
from utils.utils import logger, run_in_new_process
from utils.data import Results
from typing import Union


class ComparativeAnalysisFunctions(ComparativeHistogram, ABC):
    def __init__(self, user_id:int, user_data:dict) -> None:
        self.user_data = user_data
        self.user_id = user_id
        ComparativeHistogram.__init__(user_id, user_data, self.values)
        ABC.__init__(self)

    def comparative_analysis(self) -> dict:
        try:
            extremums = self.__calc_extremums()
            interval_mode = self.__calc_interval_mode()    
            process, queue = run_in_new_process(self.create_histogram)
            process.join()
            hist_path = queue.get()
            return self.__results_formater(hist_path, extremums, interval_mode)
        except Exception as e:
            logger.error(f"\nError in {self.__class_.__name__} \
                {currentframe().f_code.co_name}: {e}", exc_info=True)
            return self.__results_formater(exc=True)

    def __calc_extremums(self) -> dict[str, int]:
        mu = Decimal(np.mean(self.values))
        sigma = Decimal(np.std(self.values))
        weights = np.array([Decimal(1) / (sigma * Decimal(math.sqrt(2 * math.pi))) * \
            Decimal(math.exp(- (x - mu) ** 2 / (2 * sigma ** 2))) for x in self.values])
        weighted_mean = np.average(self.values, weights=weights)
        weighted_sum = np.sum(weights * (self.values - weighted_mean) ** 2)
        weighted_std_dev = Decimal(math.sqrt(weighted_sum / np.sum(weights)))
        return {
            'high': int(weighted_std_dev + weighted_mean),
            'low': int(- weighted_std_dev + weighted_mean)
        }

    def __calc_interval_mode(self) -> dict:
        q, q = np.percentile(self.comp_list, [25, 75])
        iqr = q - q
        interval_width = round((2 * iqr) / (len(self.comp_list) ** (1/3)))
        intervals = list(range(min(self.comp_list), max(self.comp_list) + interval_width, interval_width))
        # sourcery skip: simplify-constant-sum
        counts = [sum(1 for price in self.comp_list if interval <= price < interval + interval_width) for interval in intervals]
        return intervals[counts.index(max(counts))] + interval_width / 2

    def __results_formater(self, hist_path: str = None, extremums: dict = None, interval_mode: Union[float, int] = None, exc: bool = None) -> Results:
        if self.regions:
            return Results(
                hist_path_regions=None if exc else hist_path,
                comp_high_regions=None if exc else extremums['high'],
                comp_low_regions=None if exc else extremums['low'],
                comp_flat_max_regions=None if exc else int(Decimal(extremums['high']) * self.user_data['area']),
                comp_flat_min_regions=None if exc else int(Decimal(extremums['low']) * self.user_data['area']),
                comp_flat_av_regions=None if exc else int(interval_mode * self.user_data['area'])
            )
        return Results(
            hist_path_streets=None if exc else hist_path,
            comp_high_streets=None if exc else extremums['high'],
            comp_low_streets=None if exc else extremums['low'],
            comp_flat_max_streets=None if exc else int(Decimal(extremums['high']) * self.user_data['area']),
            comp_flat_min_streets=None if exc else int(Decimal(extremums['low']) * self.user_data['area']),
            comp_flat_av_streets=None if exc else int(interval_mode * self.user_data['area'])
        )