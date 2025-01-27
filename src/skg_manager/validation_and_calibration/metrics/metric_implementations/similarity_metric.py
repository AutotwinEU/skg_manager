from scipy.stats import stats

from ..metric_interfaces import MetricInterface
from ...ecdfs import ECDF



class SimilarityMetric(MetricInterface):
    def calculate(self, gt_dist: ECDF, sim_dist: ECDF):
        difference = stats.wasserstein_distance(gt_dist.get_values(), sim_dist.get_values())

        if gt_dist.get_sample_size() == 0 or sim_dist.get_sample_size() == 0:
            return 1

        maximum = max(gt_dist.get_max_value(), sim_dist.get_max_value())
        if maximum == 0:
            return 1

        sim = 1 - (difference / maximum)
        return sim

    def __str__(self):
        return "similarityScore"

    def get_name(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def get_optimization_direction(self):
        return "MAX"
