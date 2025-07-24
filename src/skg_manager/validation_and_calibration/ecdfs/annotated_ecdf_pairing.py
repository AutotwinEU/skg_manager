import os
from typing import List, Optional
from matplotlib import pyplot
from pandas import DataFrame
from promg import Query

from .annotated_ecdf import AnnotatedECDF
from ..measures.measure_interfaces.measure_interface import MeasureInterface


# a collection of Ecdf_s plus a title, e.g., for plotting on the screen or write as image to file
class AnnotatedEcdfPairing:
    def __init__(self, title="", measures: Optional[List[MeasureInterface]] = None):
        # EV: Sort the different graphs on the gt_sim value.
        self.__title = title
        self.__measures = measures
        self.__gt_dist: Optional[AnnotatedECDF] = None
        self.__sim_dist: Optional[AnnotatedECDF] = None
        self.__measure_results = None

    def get_gt_dist(self):
        return self.__gt_dist

    def get_sim_dist(self):
        return self.__sim_dist

    def get_distributions(self):
        distributions = [self.__gt_dist, self.__sim_dist]
        return [dist for dist in distributions if dist is not None]

    def get_measure_results(self):
        if self.__measure_results is None:
            self.calculate_measures()
        return self.__measure_results

    def return_title(self):
        return self.__title

    def get_key(self):
        return [self.__gt_dist.get_legend(), self.__sim_dist.get_legend()]

    def calculate_measures(self):
        self.__measure_results = {}

        if self.__gt_dist is None or self.__sim_dist is None:
            return
        else:
            for measure in self.__measures:
                measure_value = measure.calculate(self.__gt_dist, self.__sim_dist)
                self.__measure_results[measure.get_name()] = measure_value

    def add_dist(self, dist):
        if dist.get_gt_sim() == "gt":
            if self.__gt_dist is None:
                self.__gt_dist = dist
            else:
                raise ValueError("Ground truth distribution has already been added.")
        else:  # get_gt_sim == "sim"
            if self.__sim_dist is None:
                self.__sim_dist = dist
            else:
                raise ValueError("Simulation distribution has already been added.")

    def get_dists_to_store_in_skg(self):
        serialized_ecdfs = []
        for dist in self.get_distributions():
            serialized_ecdfs.append({
                "legend": dist.get_legend(),
                "key": dist.get_key(),
                "gt_sim": dist.get_gt_sim(),
                "serialized_ecdf": dist.get_serialized_object(),
                "min": dist.get_min_value(),
                "max": dist.get_max_value(),
                "average": dist.get_avg_value(),
                "median": dist.get_median_value(),
                "linked_element_id": dist.get_linked_element_id(),
                "entity_type": dist.get_entity_type()
            })
        return serialized_ecdfs

    def plot_to_file(self, working_dir, dpi=80, _format="svg", show=False):
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        plot = self.plot()
        file_name = working_dir + "/" + self.return_title() + "." + _format
        plot.ioff()
        plot.savefig(file_name, dpi=dpi, format=_format)

        if show:
            plot.show()

    def plot(self):
        pyplot.clf()
        legend = []
        for dist in self.get_distributions():
            legend = dist.plot_cdf(legend)

        pyplot.legend(legend, loc="lower right", fontsize="6")
        pyplot.title(self.return_title())
        return pyplot

    def get_distribution_characteristics_table(self):
        dist_data = [dist.as_dict() for dist in self.get_distributions()]
        df_dist_data = DataFrame(dist_data)
        return df_dist_data

    def get_measure_comparison_table(self):
        measure_results = self.get_measure_results()
        measure_df = DataFrame([measure_results])
        return measure_df

