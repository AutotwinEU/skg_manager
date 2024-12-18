from typing import List, Dict, Optional

from promg import DatabaseConnection
from promg.modules.db_management import DBManagement

from ..queries.event_log_query_library import EventLogExtractorQueryLibrary as event_log_ql
from ..queries.index_query_library import IndexQueryLibrary as iql
from ..queries.statistics_query_library import StatisticsQueryLibrary as sql
from ..service_interfaces.db_manager_interface import DatabaseManagerInterface


class SKGDatabaseHelper(DBManagement, DatabaseManagerInterface):

    def __init__(self, db_connection: DatabaseConnection, semantic_header=None):
        super().__init__(db_connection, semantic_header)

    def test_connection(self):
        return self.connection.driver._driver.verify_connectivity()

    def set_constraints(self, entity_key_name="sysId") -> None:
        super().set_constraints(entity_key_name)
        self.connection.exec_query(iql.get_set_record_include_range_query)

    def _get_log_statistics(self) -> List[Dict[str, any]]:
        """
        Get the count of nodes per label and the count of relationships per type

        Returns:
            A list containing dictionaries with the label/relationship and its count
        """

        def make_empty_list_if_none(_list: Optional[List[Dict[str, str]]]):
            if _list is not None:
                return _list
            else:
                return []

        record_count = self.connection.exec_query(sql.get_record_layer_statistics)

        result = make_empty_list_if_none(record_count)

        return result

    def get_timespan(self):
        result = self.connection.exec_query(sql.get_time_span_query)
        return result

    def get_ground_truth_records_time_span(self):
        result = self.connection.exec_query(sql.get_time_span_of_ground_truth_records_query)
        return result

    def get_statistics(self) -> List[Dict[str, any]]:
        """
        Get the count of nodes per label and the count of relationships per type

        Returns:
            A list containing dictionaries with the label/relationship and its count
        """

        def make_empty_list_if_none(_list: Optional[List[Dict[str, str]]]):
            if _list is not None:
                return _list
            else:
                return []

        record_count = self.connection.exec_query(sql.get_record_layer_statistics)
        node_count = self.connection.exec_query(sql.get_node_count_query)
        edge_count = self.connection.exec_query(sql.get_edge_count_query)

        result = \
            make_empty_list_if_none(record_count) + \
            make_empty_list_if_none(node_count) + \
            make_empty_list_if_none(edge_count)

        return result

    def get_model_ids(self):
        model_ids = self.connection.exec_query(sql.get_model_ids_query)
        return model_ids

    def get_event_log(self, entity_type):
        """
        Create event_log
        """
        event_log = self.connection.exec_query(event_log_ql.get_create_event_log_query,
                                               **{
                                                   "df_type": "DF_CONTROL_FLOW_ITEM",
                                                   "entity_type": entity_type
                                               })
        return event_log
