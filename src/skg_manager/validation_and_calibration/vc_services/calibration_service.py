from abc import ABC, abstractmethod

from ..vc_service_interfaces import CalibrationServiceInterface
from ...generic.queries.performance_queries import PerformanceQueryLibrary as pql


class CalibrationService(CalibrationServiceInterface):

    def on_evaluate_measures(self, ecdf_type):
        measure_results = self.db_connection.exec_query(
            pql.get_measures_query,
            **{"ecdf_type": ecdf_type}
        )
        print(measure_results)
