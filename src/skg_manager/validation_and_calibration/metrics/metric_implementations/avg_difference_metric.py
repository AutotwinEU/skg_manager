from ..metric_interfaces import MetricInterface
from ...ecdfs import ECDF


class AverageDifferenceMetric(MetricInterface):
    def calculate(self, gt_dist: ECDF, sim_dist: ECDF):
        # returns the Kolmogorov distance between two eCDFs
        return abs(gt_dist.get_avg_value() - sim_dist.get_avg_value())

    def __str__(self):
        return "averageDifference"

    def get_name(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def get_optimization_direction(self):
        return "MIN"
