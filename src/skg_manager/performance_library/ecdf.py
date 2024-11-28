import codecs
import gzip
import pickle
from typing import List

import math
import numpy as np
from scipy.stats import stats


# an Ecdf represented by a set of values
class Ecdf:
    # EV: Added gt_sim
    def __init__(self, values: List[float]):
        self.__sample = values
        if len(self.__sample) == 0:
            self.__sample.append(0)

    def get_serialized_object(self):
        step1 = pickle.dumps(self)
        step2 = gzip.compress(step1)
        step3 = codecs.encode(step2, "base64").decode()
        return step3

    # prints the values of the eCDF textually
    def print(self):
        for v in self.__sample:
            print(str(v) + " ", end="")
        print("")

    def get_cdf_data(self):
        # calculate the cdf
        # https://how2matplotlib.com/how-to-calculate-and-plot-a-cumulative-distribution-function-with-matplotlib-in
        # -python.html
        sorted_data = np.sort(self.__sample)
        y = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        return sorted_data, y

    # returns the value of the eCDF
    def get_sample(self):
        return self.__sample

    # returns the number of values of the eCDF
    def get_sample_size(self):
        return len(self.__sample)

    # returns the minimum value of the eCDF
    def get_min_value(self):
        return np.min(self.__sample)

    # returns the median value of the eCDF
    def get_median_value(self):
        return np.median(self.__sample)

    # returns the average value of the eCDF
    def get_avg_value(self):
        return np.mean(self.__sample)

    # returns the maximum value of the eCDF
    def get_max_value(self):
        return np.max(self.__sample)

    def determine_wasserstein_distance(self, other: 'Ecdf'):
        return stats.wasserstein_distance(self.get_sample(), other.get_sample())

    # returns the similarity between two eCDFs based on the surface difference
    def determine_similarity(self, other: 'Ecdf', difference=None):
        if difference is None:
            difference = self.determine_wasserstein_distance(other)

        if self.get_sample_size() == 0 or other.get_sample_size() == 0:
            return 1

        maximum = max(self.get_max_value(), other.get_max_value())
        if maximum == 0:
            return 1

        sim = 1 - (difference / maximum)
        return sim

    def find_value_by_relative_position(self, probability: float):
        index = math.floor(probability * self.get_sample_size())
        return self.__sample[index]

    # compares two eCDFs for performance_library based on their ratio for a certain probability
    # -1 means the second eCDF performs superior
    # 0 means they perform equally
    # 1 means the first eCDFs performs superior
    def determine_performance_ratio(self, other: 'Ecdf', probability=0.5):
        value_1 = self.find_value_by_relative_position(probability)
        value_2 = other.find_value_by_relative_position(probability)
        if value_1 == 0 and value_2 == 0:
            return 0
        elif value_1 <= value_2:
            return 1 - (value_1 / value_2)
        else:
            return - 1 + (value_2 / value_1)

    # returns the Kolmogorov distance between two eCDFs
    def determine_kolmogorov(self, other: 'Ecdf'):
        return stats.ks_2samp(self.get_sample(), other.get_sample()).pvalue
