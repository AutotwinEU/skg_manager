import codecs
import gzip
import pickle
from typing import List

import numpy as np


# an Ecdf represented by a set of values
class ECDF:
    # EV: Added gt_sim
    def __init__(self, values: List[float]):
        self.__values = values
        if len(self.__values) == 0:
            self.__values.append(0)

    def get_serialized_object(self):
        step1 = pickle.dumps(self)
        step2 = gzip.compress(step1)
        step3 = codecs.encode(step2, "base64").decode()
        return step3

    @classmethod
    def deserialize(cls, serialized_object):
        step1 = codecs.decode(serialized_object.encode(), "base64")
        step2 = gzip.decompress(step1)
        step3 = pickle.loads(step2)  # This will return the deserialized object
        if isinstance(step3, cls):  # Ensure the deserialized object is of the correct type
            return step3
        else:
            raise TypeError("Deserialized object is not of type {}".format(cls.__name__))

    # prints the values of the eCDF textually
    def print(self):
        for v in self.__values:
            print(str(v) + " ", end="")
        print("")

    def get_cdf_data(self):
        # calculate the cdf
        # https://how2matplotlib.com/how-to-calculate-and-plot-a-cumulative-distribution-function-with-matplotlib-in
        # -python.html
        sorted_data = np.sort(self.__values)
        y = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        return sorted_data, y

    # returns the value of the eCDF
    def get_values(self):
        return self.__values

    # returns the number of values of the eCDF
    def get_sample_size(self):
        return len(self.__values)

    # returns the minimum value of the eCDF
    def get_min_value(self):
        return np.min(self.__values)

    # returns the median value of the eCDF
    def get_median_value(self):
        return np.median(self.__values)

    # returns the average value of the eCDF
    def get_avg_value(self):
        return np.mean(self.__values)

    # returns the maximum value of the eCDF
    def get_max_value(self):
        return np.max(self.__values)
