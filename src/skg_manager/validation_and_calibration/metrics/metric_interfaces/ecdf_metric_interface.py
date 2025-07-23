import logging
from abc import ABC, abstractmethod
from typing import List

from promg import DatabaseConnection, Query

from .helper_functions import check_start_and_end_times
from .metric_interface import MetricInterface
from ....generic.queries.performance_queries import PerformanceQueryLibrary as pfql

from ...measures.measure_interfaces import MeasureInterface
from ...ecdfs import AnnotatedECDF, AnnotatedEcdfPairing, ECDF

error_message = "No database connection found, have you set it?"


class EcdfMetricInterface(MetricInterface, ABC):
    def __init__(self, name: str, measures: List[MeasureInterface]):
        super().__init__(name=name, measures=measures)

    # Implement Abstract Methods of MetricInterface
    def calculate_result(self, start_time=None, end_time=None):
        self.remove_ecdfs_from_skg()
        self.calculate_ecdfs_from_skg(start_time=start_time, end_time=end_time)
        self.add_ecdfs_to_skg()

    def clear_result(self):
        self.result = {}

    def generate_html_content(self):
        if self.result is None:
            self.retrieve_ecdfs_from_skg()

        self.html_content = f"<h2>Ecdf for {self.get_name()}</h2>\n"
        for index, ecdf_pairing in enumerate(self.result.values()):
            ecdf_pairing.plot_to_file("static/figures", show=False)
            ecdf_data = ecdf_pairing.get_distribution_characteristics_table()
            conformance_data = ecdf_pairing.get_measure_comparison_table()
            self.html_content += f'''
                <h4 id='eCDF {index}'> {self.get_name()}: {ecdf_pairing.return_title()} </h4>
                
                <img src='../static/figures/{ecdf_pairing.return_title()}.svg'><a href='#top'>back to top</a><br><br>
                Aggregate values:<br>
                {ecdf_data.to_html(index=False, justify="left")}'''

            if not conformance_data.empty:
                self.html_content += f'''
                <br>Metric results:<br>
                {conformance_data.to_html(index=False, justify="left")}
                '''

    ####################
    # Abstract Methods #
    ####################

    @abstractmethod
    def extract_ecdf_query_function(self, start_time="1970-01-01 00:00:00", end_time="2970-01-01 23:59:59") -> Query:
        """
        Provide a Query object that finds a list of numerical values (samples) for which an ecdf can be created.
        The query should return the following information
        - key --> the ecdf describes the distribution of an object, the key is a unique description of this object
        which can be understood by humans
        - element_id --> the ecdf describes the distribution of an object, the element_id is id of the object in the skg
        - is_simulated_data --> the ecdf is retrieved for simulated data or ground truth data
        - entity_type --> the entity_type for which the distribution is calculated
        - dist_values --> the values of the ecdf (a list of numerical values)

        :param start_time: start time of interval formatted as "yyyy-MM-dd HH:mm:ss"
        :param end_time: end time of interval formatted as "yyyy-MM-dd HH:mm:ss"
        :return: Query object that finds a list of numerical values
        """

        pass

    ## Additional Implementations

    # Calculate the ECDF
    def calculate_ecdfs_from_skg(self, start_time=None, end_time=None):
        if not self.check_db_connection():
            raise ValueError(error_message)

        # find all ecdfs for which a calculation has to be made
        self.clear_result()
        start_time, end_time = check_start_and_end_times(start_time, end_time)
        try:
            results = self.db_connection.exec_query(self.extract_ecdf_query_function,
                                                    **{
                                                        "start_time": start_time,
                                                        "end_time": end_time
                                                    })

            logging.debug(
                f"Distribution {self.get_name()} fetched for "
                f"{start_time if start_time is not None else ''} - {end_time if end_time is not None else ''} : "
                f"{results}")

            if not results or len(results) == 0:
                logging.warning("No execution times found")
                return None  # Early return if no data is found

            for skg_result in results:
                distribution = AnnotatedECDF.create_from_query_result(query_result=skg_result,
                                                                      ecdf_name=self.get_name())
                self.add_ecdf_to_result(distribution)

        except Exception as e:
            logging.error(f"Error in execution times between sensors: {str(e)}",
                          exc_info=True)

    def add_ecdf_to_result(self, ecdf):
        key = ecdf.get_key()

        if key in self.result:
            distribution_pairing = self.result[key]
            distribution_pairing.add_dist(ecdf)
        else:
            distribution_pairing = AnnotatedEcdfPairing(title=key,
                                                        measures=self.measures)
            distribution_pairing.add_dist(ecdf)
            self.result[key] = distribution_pairing

    # Store the ECDFS in SKG
    def add_ecdfs_to_skg(self):
        if not self.check_db_connection():
            raise ValueError(error_message)

        for distribution_pairing in self.result.values():
            self.db_connection.exec_query(distribution_pairing.get_store_pairing_in_skg_query)

        print("finish add_performance_to_skg")

    # Retrieve the ECDFS from SKG
    def retrieve_ecdfs_from_skg(self):
        if not self.check_db_connection():
            raise ValueError("No database connection found, have you set it?")

        ecdfs_from_skg = self.db_connection.exec_query(pfql.retrieve_distributions,
                                                       **{"_type": self.get_name()})

        if ecdfs_from_skg is None or len(ecdfs_from_skg) == 0:
            self.calculate_ecdfs_from_skg()
        else:
            self.clear_result()
            for ecdf in ecdfs_from_skg:
                deserialized_ecdf = ECDF.deserialize(ecdf)
                self.add_ecdf_to_result(deserialized_ecdf)

    # Remove the ECDFS from SKG
    def remove_ecdfs_from_skg(self):
        if not self.check_db_connection():
            raise ValueError(error_message)

        self.db_connection.exec_query(pfql.delete_ecdf_nodes,
                                      **{"_type": self.get_name()})
