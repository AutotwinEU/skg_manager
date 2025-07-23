from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import pandas as pd
from flask import send_from_directory, Response, render_template
from promg import DatabaseConnection

from ..service_interfaces.calibration_validation_interface import \
    ValidationAndCalibrationServiceInterface
from ..queries.performance_queries import PerformanceQueryLibrary as pql
from ...validation_and_calibration import MetricInterface


class ValidationAndCalibrationService(ValidationAndCalibrationServiceInterface):
    def __init__(self, db_connection: DatabaseConnection, metrics: List[MetricInterface]):
        self.db_connection = db_connection
        self.metrics = metrics
        self.tabs = []

    def render_validation_template(self) -> Response:
        metrics = [metric.get_dict_repr() for metric in self.metrics]
        return render_template('performance_results.html',
                               metrics=metrics)

    def calculate_performance(self, start_date=None, end_date=None):
        for metric in self.metrics:
            metric.set_db_connection(self.db_connection)
            metric.calculate_result(start_time=start_date, end_time=end_date)

    def retrieve_mean(self, ecdf_type):
        measure_results = self.db_connection.exec_query(
            pql.get_measures_query,
            **{"ecdf_type": ecdf_type}
        )

        print(measure_results)

        pivot_results = {}

        for measure_result in measure_results:
            _type = measure_result["ecdf_type"]
            measures = measure_result["measures"]
            df_measures = pd.DataFrame(measures)
            mean_df_measures = df_measures.mean()
            mean_dict = mean_df_measures.to_dict()
            pivot_results[_type] = mean_dict

        return pivot_results

    def get_ecdf_types(self):
        ecdf_types = []
        for ecdf_wrapper in self.metrics:
            ecdf_types.append(ecdf_wrapper.get_name())
        return ecdf_types

    def get_measure_names(self, metric_name: Optional[str] = None):
        measures = {}
        for metric in self.metrics:
            if metric_name is None or metric_name == metric.get_name():
                measures[metric.get_name()] = metric.get_measures()
        return measures
