from scipy.stats import stats

from ..metric_interfaces import MetricInterface
from ...ecdfs import ECDF


class WassersteinDistanceMetric(MetricInterface):
    def calculate(self, gt_dist: ECDF, sim_dist: ECDF):
        return stats.wasserstein_distance(gt_dist.get_values(), sim_dist.get_values())

    def __str__(self):
        return "wassersteinDistance"

    def get_name(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def get_optimization_direction(self):
        return "MIN"