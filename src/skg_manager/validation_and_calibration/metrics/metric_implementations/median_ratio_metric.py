from ..metric_interfaces import MetricInterface
from ...ecdfs import ECDF



class MedianRatioMetric(MetricInterface):

    # compares two eCDFs for performance_library based on their ratio for a certain probability
    # -1 means the second eCDF performs superior
    # 0 means they perform equally
    # 1 means the first eCDFs performs superior
    def calculate(self, gt_dist: ECDF, sim_dist: ECDF):
        gt_median = gt_dist.get_median_value()
        sim_median = sim_dist.get_median_value()

        if gt_median == 0 and sim_median == 0:
            return 0
        elif gt_median <= sim_median:
            return 1 - (gt_median / sim_median)
        else:
            return - 1 + (sim_median / gt_median)

    def __str__(self):
        return "medianRatio"

    def get_name(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()
