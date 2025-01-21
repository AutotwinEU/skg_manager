from abc import ABC, abstractmethod
from datetime import datetime

from promg import Query
from skg_manager.generic.queries.performance_queries import PerformanceQueryLibrary as pfql


class EcdfServiceInterface(ABC):

    def __init__(self, db_connection, type):
        self.db_connection = db_connection
        self._type = type

    @staticmethod
    def check_is_date(timestamp):
        try:
            is_date = bool(datetime.strptime(timestamp, "%Y-%m-%d"))
        except ValueError:
            is_date = False
        return is_date

    @staticmethod
    def check_datetime_is_correct_format(timestamp):
        try:
            is_date_time = bool(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            is_date_time = False
        return is_date_time

    def check_start_and_end_times(self, start_time, end_time):
        if start_time is None:
            start_time = "1970-01-01 00:00:00"
        if end_time is None:
            end_time = "2970-01-01 23:59:59"

        if self.check_is_date(start_time):  # add hours et cetera
            start_time = f"{start_time} 00:00:00"
        if self.check_is_date(end_time):  # add hours et cetera
            end_time = f"{end_time} 23:59:59"

        if not self.check_datetime_is_correct_format(start_time):
            raise ValueError(
                f"start_time: {start_time} is of incorrect format, it should be %Y-%m-%d or %Y-%m-%d %H:%M:%S")

        if not self.check_datetime_is_correct_format(end_time):
            raise ValueError(
                f"start_time: {end_time} is of incorrect format, it should be %Y-%m-%d or %Y-%m-%d %H:%M:%S")

        return start_time, end_time

    def extract_ecdfs_from_skg(self, start_time=None, end_time=None):
        start_time, end_time = self.check_start_and_end_times(start_time, end_time)

        return self.db_connection.exec_query(self.extract_ecdf_query_function,
                                             **{
                                                 "start_time": start_time,
                                                 "end_time": end_time
                                             })

    def add_ecdf_nodes_to_skg(self, distribution_pairing):
        self.db_connection.exec_query(distribution_pairing.get_store_pairing_in_skg_query)

    def remove_ecdf_nodes_from_skg(self):
        self.db_connection.exec_query(pfql.delete_ecdf_nodes,
                                      **{"_type": self._type})

    def retrieve_ecdf_nodes_from_skg(self):
        return self.db_connection.exec_query(pfql.retrieve_distributions,
                                             **{"_type": self._type})

    def get_type(self):
        return self._type

    @abstractmethod
    def extract_ecdf_query_function(self, start_time="1970-01-01 00:00:00", end_time="2970-01-01 23:59:59") -> Query:
        """
        Provide a Query object that finds a list of numerical values (samples) for which a an ecdf can be created.
        The query should return the following information
        - element_id --> the ecdf describes the distribution of an object, the element_id is id of the object in the skg
        - key --> the ecdf describes the distribution of an object, the key is a unique description of this object
        which can be understood by humans
        - is_simulated_data --> the ecdf is retrieved for simulated data or ground truth data
        - entity_type --> the entity_type
        - dist_values --> the values of the ecdf (a list of numerical values)

        :param start_time: start time of interval formatted as "yyyy-MM-dd HH:mm:ss"
        :param end_time: end time of interval formatted as "yyyy-MM-dd HH:mm:ss"
        :return: Query object that finds a list of numerical values
        """

        pass
