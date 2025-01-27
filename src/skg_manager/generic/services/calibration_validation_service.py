from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd
from promg import DatabaseConnection

from ..service_interfaces.calibration_validation_interface import \
    ValidationAndCalibrationServiceInterface
from ..queries.performance_queries import PerformanceQueryLibrary as pql
from ...validation_and_calibration import EcdfWrapperInterface


class ValidationAndCalibrationService(ValidationAndCalibrationServiceInterface):
    def __init__(self, db_connection: DatabaseConnection, working_dir, ecdf_wrappers: List[EcdfWrapperInterface]):
        self.db_connection = db_connection
        self.ecdf_wrappers = ecdf_wrappers
        self.working_dir = working_dir

    def calculate_performance(self, start_date=None, end_date=None):
        for ecdf_wrapper in self.ecdf_wrappers:
            ecdf_wrapper.set_db_connection(self.db_connection)
            ecdf_wrapper.remove_ecdfs_from_skg()
            ecdf_wrapper.calculate_ecdfs_from_skg(start_time=start_date, end_time=end_date)
            ecdf_wrapper.add_ecdfs_to_skg()
            ecdf_wrapper.create_aggregated_performance_html(self.working_dir)

    def retrieve_mean_metrics(self, ecdf_type):
        metric_results = self.db_connection.exec_query(
            pql.get_get_metrics_query,
            **{"ecdf_type": ecdf_type}
        )

        print(metric_results)

        pivot_results = {}

        for metric_result in metric_results:
            _type = metric_result["ecdf_type"]
            metrics = metric_result["metrics"]
            df_metrics = pd.DataFrame(metrics)
            mean_df_metrics = df_metrics.mean()
            mean_dict = mean_df_metrics.to_dict()
            pivot_results[_type] = mean_dict

        return pivot_results

    def get_ecdf_types(self):
        ecdf_types = []
        for ecdf_wrapper in self.ecdf_wrappers:
            ecdf_types.append(ecdf_wrapper.get_ecdf_type())
        return ecdf_types

    def get_metric_names(self, ecdf_type: Optional[str] = None):
        metrics = {}
        for ecdf_wrapper in self.ecdf_wrappers:
            _type = ecdf_wrapper.get_ecdf_type()
            if ecdf_type is None or ecdf_type == _type:
                metrics[_type] = ecdf_wrapper.get_metrics()
        return metrics
