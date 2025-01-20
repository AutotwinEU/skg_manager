from matplotlib import pyplot

from .ecdf import ECDF


class AnnotatedECDF(ECDF):
    def __init__(self, key, values, _type, element_id, legend="", gt_sim="gt"):
        super().__init__(values)
        self.__key = key
        self.__type = _type
        self.__legend = legend
        self.__gt_sim = gt_sim

        self._linked_element_id = element_id

    # add magic method for sorting
    def __lt__(self, other):
        return self.__legend < other.get_legend()

    def get_label_color(self):
        if self.get_gt_sim() == "gt":
            return "blue"
        else:
            return "orange"

    def plot_cdf(self, legend):
        legend.append(self.get_gt_sim())
        x, y = self.get_cdf_data()

        pyplot.plot(x, y, c=self.get_label_color(), alpha=0.7)
        return legend

    # returns the legend of the eCDF
    def get_legend(self):
        return self.__legend

    # changes the legend of the eCDF
    def set_legend(self, legend):
        self.__legend = legend

    # returns the associated sensors of an Ecdf
    def get_key(self):
        return self.__key

    # EV: Add getter for gt_sim
    def get_gt_sim(self):
        return self.__gt_sim

    def get_linked_element_id(self):
        return self._linked_element_id

    def get_type(self):
        return self.__type

    def as_dict(self):
        return {
            'design': self.get_legend(), 'min': self.get_min_value(), 'max': self.get_max_value(),
            'mean': self.get_avg_value(), 'median': self.get_median_value()
        }
