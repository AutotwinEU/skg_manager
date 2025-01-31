import os
from typing import List, Optional
from matplotlib import pyplot
from pandas import DataFrame
from promg import Query

from .annotated_ecdf import AnnotatedECDF
from skg_manager.validation_and_calibration.metrics.metric_interfaces.metric_interface import MetricInterface


# a collection of Ecdf_s plus a title, e.g., for plotting on the screen or write as image to file
class AnnotatedEcdfPairing:
    def __init__(self, title="", metrics: Optional[List[MetricInterface]] = None):
        # EV: Sort the different graphs on the gt_sim value.
        self.__title = title
        self.__metrics = metrics
        self.__gt_dist: Optional[AnnotatedECDF] = None
        self.__sim_dist: Optional[AnnotatedECDF] = None
        self.__metric_results = None

    def get_gt_dist(self):
        return self.__gt_dist

    def get_sim_dist(self):
        return self.__sim_dist

    def get_distributions(self):
        distributions = [self.__gt_dist, self.__sim_dist]
        return [dist for dist in distributions if dist is not None]

    def get_metric_results(self):
        if self.__metric_results is None:
            self.calculate_metrics()
        return self.__metric_results

    def return_title(self):
        return self.__title

    def get_key(self):
        return [self.__gt_dist.get_legend(), self.__sim_dist.get_legend()]

    def calculate_metrics(self):
        self.__metric_results = {}

        if self.__gt_dist is None or self.__sim_dist is None:
            return
        else:
            for metric in self.__metrics:
                metric_value = metric.calculate(self.__gt_dist, self.__sim_dist)
                self.__metric_results[metric.get_name()] = metric_value

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

    def get_metric_comparison_table(self):
        metric_data = self.get_metric_results()
        metric_data = DataFrame([metric_data])
        return metric_data

    def get_type(self):
        if self.__gt_dist is not None:
            return self.__gt_dist.get_type()
        if self.__sim_dist is not None:
            return self.__sim_dist.get_type()
        return None

    def get_store_pairing_in_skg_query(self):
        query_str = '''
            UNWIND $distributions as ecdf_info
            CALL {WITH ecdf_info
                  MATCH (linkedElement) 
                  MATCH (et:EntityType {entityType: ecdf_info.entity_type})
                  WHERE elementId(linkedElement) = ecdf_info.linked_element_id  
                     
                  MERGE (linkedElement) - [:HAS_DISTRIBUTION] -> (ecdf:ECDF {type: $type, key: ecdf_info.key}) 
                    - [:OF_ENTITY_TYPE] -> (et)
                  ON CREATE SET ecdf += {name: ecdf_info.legend, 
                                source: ecdf_info.gt_sim,
                                value: ecdf_info.serialized_ecdf,
                                min: ecdf_info.min,
                                max: ecdf_info.max,
                                average: ecdf_info.average,
                                median: ecdf_info.median
                                }
                  RETURN ecdf
            }
            WITH ecdf
            WITH collect(ecdf) as ecdfs
            WHERE size(ecdfs) > 1
            WITH CASE
            WHEN ecdfs[0].source = "gt" THEN ecdfs[0]
            ELSE ecdfs[1] 
            END AS gt_ecdf,
            CASE
            WHEN ecdfs[0].source = "sim" THEN ecdfs[0]
            ELSE ecdfs[1] 
            END AS sim_ecdf
            
            MERGE (gt_ecdf) - [metric:COMPARES_TO] -> (sim_ecdf)
            SET metric = $metric_results
        '''

        return Query(query_str=query_str,
                     parameters={
                         "name": self.__title,
                         "type": self.get_type(),
                         "distributions": self.get_dists_to_store_in_skg(),
                         "metric_results": self.get_metric_results()
                     })
