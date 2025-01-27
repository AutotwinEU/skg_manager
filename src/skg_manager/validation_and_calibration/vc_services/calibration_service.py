from abc import ABC, abstractmethod

from ..vc_service_interfaces import CalibrationServiceInterface


class CalibrationService(CalibrationServiceInterface):

    def on_evaluate_metrics(self, ecdf_type):
        metric_results = self.db_connection.exec_query(
            pql.get_get_metrics_query,
            **{"ecdf_type": ecdf_type}
        )
        print(metric_results)
