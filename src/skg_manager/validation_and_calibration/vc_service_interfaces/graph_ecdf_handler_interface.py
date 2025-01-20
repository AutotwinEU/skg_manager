from abc import ABC, abstractmethod

from promg import Query
from skg_manager.generic.queries.performance_queries import PerformanceQueryLibrary as pfql


class GraphEcdfHandlerInterface(ABC):

    def __init__(self, db_connection, type):
        self.db_connection = db_connection
        self._type = type

    def extract_ecdfs_from_skg(self, time_interval=None):
        return self.db_connection.exec_query(self.extract_ecdf_query_function,
                                             **{"time_interval": time_interval})

    def add_ecdf_nodes_to_skg(self, distribution_pairing):
        self.db_connection.exec_query(distribution_pairing.get_store_pairing_in_skg_query)

    def remove_ecdf_nodes_from_skg(self):
        self.db_connection.exec_query(pfql.delete_ecdf_nodes,
                                      **{"type": self._type})

    def retrieve_ecdf_nodes_from_skg(self):
        return self.db_connection.exec_query(pfql.retrieve_distributions,
                                             **{"_type": self._type})

    def get_type(self):
        return self._type

    @abstractmethod
    def extract_ecdf_query_function(self, time_interval=None) -> Query:
        pass
