from statistics import stdev
from inspect import currentframe
from cost_comp_analysis.calculating.cost_analysis import CostAnalysisFunctions 
from cost_comp_analysis.calculating.comparative_analysis import ComparativeAnalysisFunctions
from utils.utils import logger
from utils.data import Results, CostCompDataClass

class CostComparativeAnalysisFunctions(CostCompDataClass, ComparativeAnalysisFunctions, CostAnalysisFunctions):
    def __init__(self, user_id:int, user_data:dict, comp_list_regions:list, comp_list_streets:list) -> None:
        CostCompDataClass.__init__(self)
        ComparativeAnalysisFunctions.__init__(self, user_id, user_data, comp_list_regions, comp_list_streets)
        CostAnalysisFunctions.__init__(self, user_data)


    def results(self) -> Results:
        self.regions = True
        results = Results.merge_results(
            self.cost_analysis(),
            self.comparative_analysis()
        )
        self.toggle_regions()
        results = Results.merge_results(results,self.comparative_analysis())
        return Results.merge_results(results, self.__final_results(results))


    def __final_results(self, results:Results) -> Results:
        try:
            filtered_values = [value for value in results.values() if value != 0]
            price_dev = stdev(filtered_values)
            av_flat_price = int((results.comp_flat_av_regions + results.comp_flat_av_streets + (results.av_flat_cost_price * 5)) / 7)
        except Exception as e:
            logger.error(f"\nError in {self.__class_.__name__} \
                {currentframe().f_code.co_name}: \n{e}", exc_info=True)
            price_dev = 0
            av_flat_price = 0
        return Results(
            av_flat_price = av_flat_price,
            comb_results_max = av_flat_price + price_dev,
            comb_results_min = av_flat_price - price_dev
        )