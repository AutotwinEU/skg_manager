from ..measure_interfaces import MeasureInterface
from ...ecdfs import ECDF


class MinimumDifferenceMeasure(MeasureInterface):
    def calculate(self, gt_dist: ECDF, sim_dist: ECDF):
        # returns the Kolmogorov distance between two eCDFs
        return abs(gt_dist.get_min_value() - sim_dist.get_min_value())

    def __str__(self):
        return "minimumDifference"

    def get_name(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def get_optimization_direction(self):
        return "MIN"
