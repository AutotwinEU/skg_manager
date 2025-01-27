from scipy.stats import stats

from ..metric_interfaces import MetricInterface
from ...ecdfs import ECDF


class KolmogorovMetric(MetricInterface):
    def calculate(self, gt_dist: ECDF, sim_dist: ECDF):
        # returns the Kolmogorov distance between two eCDFs
        return stats.ks_2samp(gt_dist.get_values(), sim_dist.get_values()).pvalue

    def __str__(self):
        return "kolmogorovScore"

    def get_name(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def get_optimization_direction(self):
        return "MAX"
