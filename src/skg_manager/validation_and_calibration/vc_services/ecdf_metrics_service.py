import logging

from ..vc_service_interfaces import EcdfMetricCalculatorInterface, GraphEcdfHandlerInterface
from ..ecdfs import AnnotatedECDF, AnnotatedEcdfPairing, ECDF


class EcdfMetricsCalculator(EcdfMetricCalculatorInterface):


    def __init__(self, metric_measures, working_dir,
                 ecdf_handler: GraphEcdfHandlerInterface):

        self.ecdf_handler = ecdf_handler
        self._type = self.ecdf_handler.get_type()

        self.metric_measures = metric_measures

        self.distribution_pairings = {}
        self.working_dir = working_dir

    def clear_distribution_pairings(self):
        self.distribution_pairings = {}

    # ==============================================================================
    def calculate_ecdfs_from_skg(self, time_interval=None) -> None:
        # find all ecdfs for which a calculation has to be made
        self.clear_distribution_pairings()
        try:
            results = self.ecdf_handler.extract_ecdfs_from_skg(time_interval=time_interval)
            logging.debug(f"Execution times fetched for {time_interval}: {results}")

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

        # Create ECDF object
        distribution = AnnotatedECDF(values=dist_values,
                                     legend=f"{self._type}: {key}",
                                     key=key,
                                     element_id=element_id,
                                     _type=self._type,
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
        f.write("<h2>Ecdfcs</h2>\n")
        for index, ecdf_collection in enumerate(self.distribution_pairings.values()):
            ecdf_collection.plot_to_file(self.working_dir, show=False)
            f.write("<h4>" + ecdf_collection.return_title() + "\n")
            f.write(
                f"<a id='eCDF {index}'></h4><img src='{ecdf_collection.return_title()}.svg'><a href='#top'>back to "
                f"top<a><br>\n")

            f.write("<br>Aggregate values:<br>")
            ecdf_data = ecdf_collection.get_table_of_ecdf_aggregate()
            f.write(ecdf_data.to_html(index=False, justify="left"))

            conformance_data = ecdf_collection.get_conformance_table()
            if len(conformance_data) > 0:
                f.write("<br>Conformance values:<br>")
                f.write(conformance_data.to_html(index=False, justify="left"))
        f.close()
