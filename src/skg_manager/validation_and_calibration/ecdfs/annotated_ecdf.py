from matplotlib import pyplot

from .ecdf import ECDF


class AnnotatedECDF(ECDF):
    def __init__(self, key, values, entity_type, _type, element_id, legend="", gt_sim="gt"):
        super().__init__(values)
        self.__key = key
        self.__type = _type
        self.__legend = legend
        self.__gt_sim = gt_sim
        self.__entity_type = entity_type

        self._linked_element_id = element_id

    # add magic method for sorting
    def __lt__(self, other):
        return self.__legend < other.get_legend()

    def get_label_color(self):
        if self.is_gt():
            return "blue"
        else:
            return "orange"

    def is_gt(self):
        return self.get_gt_sim() == "gt"

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
        if self.__entity_type in self.__key:
            return self.__key
        return self.__key + '_' + self.__entity_type

    def get_entity_type(self):
        return self.__entity_type

    # EV: Add getter for gt_sim
    def get_gt_sim(self):
        return self.__gt_sim

    def get_linked_element_id(self):
        return self._linked_element_id

    def get_type(self):
        return self.__type

    def as_dict(self):
        return {
            'source': self.get_gt_sim(),
            'entity_type': self.get_entity_type(),
            'min': self.get_min_value(), 'max': self.get_max_value(),
            'mean': self.get_avg_value(), 'median': self.get_median_value()
        }
