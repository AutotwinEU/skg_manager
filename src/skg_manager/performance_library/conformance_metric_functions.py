class EcdfConformanceMetrics:
    def __init__(self, ecdf_1, ecdf_2, probability=0.5):
        self.legend = ecdf_1.get_gt_sim() + "-" + ecdf_2.get_gt_sim()
        self.difference = ecdf_1.determine_wasserstein_distance(other=ecdf_2)
        self.similarity = ecdf_1.determine_similarity(other=ecdf_2, difference=self.difference)
        self.performance = ecdf_1.determine_performance_ratio(other=ecdf_2, probability=probability)
        self.kolmogorov = ecdf_1.determine_kolmogorov(other=ecdf_2)

    def as_dict(self):
        return {
            "design": self.legend, "difference": self.difference, "similarity": self.similarity,
            "performance_library": self.performance, "kolmogorov": self.kolmogorov
        }
