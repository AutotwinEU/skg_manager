import logging
from typing import List

from ..metrics.metric_interfaces import MetricInterface
from ..vc_service_interfaces import EcdfWrapperInterface, EcdfServiceInterface
from ..ecdfs import AnnotatedECDF, AnnotatedEcdfPairing, ECDF


class EcdfWrapper(EcdfWrapperInterface):
    def __init__(self,
                 metric_measures: List[MetricInterface],
                 working_dir,
                 ecdf_handler: EcdfServiceInterface):

        self.ecdf_handler = ecdf_handler
        self._described_behavior = self.ecdf_handler.get_described_behavior()

        self.metric_measures = metric_measures

        self.distribution_pairings = {}
        self.working_dir = working_dir

    def set_db_connection(self, db_connection):
        self.ecdf_handler.set_db_connection(db_connection=db_connection)

    def clear_distribution_pairings(self):
        self.distribution_pairings = {}

    def get_ecdf_type(self):
        return self._described_behavior

    def get_metrics(self):
        result = []
        for metric_measure in self.metric_measures:
            metric = {
                "name": metric_measure.get_name(),
                "optimization_type": metric_measure.get_optimization_direction(),
            }
            result.append(metric)
        return result

    # ==============================================================================
    def calculate_ecdfs_from_skg(self, start_time=None, end_time=None) -> None:
        # find all ecdfs for which a calculation has to be made
        self.clear_distribution_pairings()
        try:
            results = self.ecdf_handler.extract_ecdfs_from_skg(start_time=start_time, end_time=end_time)
            logging.debug(
                f"Distribution {self._described_behavior} fetched for "
                f"{start_time if start_time is not None else ''} - {end_time if end_time is not None else ''} : "
                f"{results}")

            if not results or len(results) == 0:
                logging.warning("No execution times found")
                return None  # Early return if no data is found

            for skg_result in results:
                distribution = self.create_annotated_ecdf(skg_result)
                self.add_ecdf_to_pairings(distribution)

        except Exception as e:
            logging.error(f"Error in execution times between sensors: {str(e)}",
                          exc_info=True)

    def create_annotated_ecdf(self, skg_result):
        gt_sim = "sim" if skg_result['is_simulated_data'] else "gt"
        key = skg_result["key"]
        dist_values = skg_result["dist_values"]
        element_id = skg_result["element_id"]
        entity_type = skg_result["entity_type"]

        # Create ECDF object
        distribution = AnnotatedECDF(values=dist_values,
                                     legend=f"{self._described_behavior}: {key}",
                                     key=key,
                                     entity_type=entity_type,
                                     element_id=element_id,
                                     _type=self._described_behavior,
                                     gt_sim=gt_sim)
        return distribution

    def add_ecdf_to_pairings(self, ecdf):
        key = ecdf.get_key()

        if key in self.distribution_pairings:
            distribution_pairing = self.distribution_pairings[key]
            distribution_pairing.add_dist(ecdf)
        else:
            distribution_pairing = AnnotatedEcdfPairing(title=key,
                                                        metrics=self.metric_measures)
            distribution_pairing.add_dist(ecdf)
            self.distribution_pairings[key] = distribution_pairing

    def add_ecdfs_to_skg(self):
        print("start add_performance_to_skg")
        for distribution_pairing in self.distribution_pairings.values():
            self.ecdf_handler.add_ecdf_nodes_to_skg(distribution_pairing=distribution_pairing)

        print("finish add_performance_to_skg")

    def retrieve_ecdfs_from_skg(self):
        ecdfs_from_skg = self.ecdf_handler.retrieve_ecdf_nodes_from_skg()

        if ecdfs_from_skg is None or len(ecdfs_from_skg) == 0:
            self.calculate_ecdfs_from_skg()
        else:
            self.clear_distribution_pairings()
            for ecdf in ecdfs_from_skg:
                deserialized_ecdf = ECDF.deserialize(ecdf)
                self.add_ecdf_to_pairings(deserialized_ecdf)

    def remove_ecdfs_from_skg(self):
        self.ecdf_handler.remove_ecdf_nodes_from_skg()

    def create_aggregated_performance_html(self):
        if self.distribution_pairings is None:
            self.retrieve_ecdfs_from_skg()
        self.create_index_file()

    def create_index_file(self):
        f = open(self.working_dir + "/index.html", "w")
        f.write(f"<h2>Ecdf for {self._described_behavior}</h2>\n")
        for index, ecdf_pairing in enumerate(self.distribution_pairings.values()):
            ecdf_pairing.plot_to_file(self.working_dir, show=False)
            f.write("<h4>" + self._described_behavior + ": " + ecdf_pairing.return_title() + "\n")
            f.write(
                f"<a id='eCDF {index}'></h4><img src='{ecdf_pairing.return_title()}.svg'><a href='#top'>back to "
                f"top<a><br>\n")

            f.write("<br>Aggregate values:<br>")
            ecdf_data = ecdf_pairing.get_distribution_characteristics_table()
            f.write(ecdf_data.to_html(index=False, justify="left"))

            conformance_data = ecdf_pairing.get_metric_comparison_table()
            if not conformance_data.empty:
                f.write("<br>Metric results:<br>")
                f.write(conformance_data.to_html(index=False, justify="left"))
        f.close()
