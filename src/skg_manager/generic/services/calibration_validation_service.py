from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import pandas as pd
from flask import Response, render_template
from promg import DatabaseConnection

from ..service_interfaces.calibration_validation_interface import \
    ValidationAndCalibrationServiceInterface
from ...validation_and_calibration import MetricInterface
from .helper_functions import get_start_and_end_times


class ValidationAndCalibrationService(ValidationAndCalibrationServiceInterface):
    def __init__(self, db_connection: DatabaseConnection, metrics: List[MetricInterface]):
        self.db_connection = db_connection
        self.metrics = metrics
        self.tabs = []

    def render_validation_template(self) -> str:
        metric_results = []
        for metric in self.metrics:
            metric_results.append(metric.get_dict_repr())

        return render_template('performance_results.html',
                               metrics=metric_results)

    def calculate_performance(self, start_date=None, end_date=None, used_for_calibration=True):
        for metric in self.metrics:
            # first, not used_for_calibration --> determine all metrices, also those not used for calibration
            # OR calculate those metrics used for calibration
            if (not used_for_calibration) or metric.used_for_calibration:
                metric.set_db_connection(self.db_connection)
                start_time, end_time = get_start_and_end_times(start_date, end_date)
                metric.clear_result()  # ensure that the result is cleared before calculating new results
                metric.calculate_result(start_time=start_time, end_time=end_time)

    def get_metric_names(self):
        metrics = []
        for metric in self.metrics:
            metrics.append(metric.get_name())
        return metrics

    def get_measure_names(self, metric_name: Optional[str] = None):
        measures = {}
        for metric in self.metrics:
            if metric_name is None or metric_name == metric.get_name():
                measures[metric.get_name()] = metric.get_measures()
        return measures

    def retrieve_mean_of_measures(self, metric_name: Optional[str] = None):
        pivot_results = {}
        for metric in self.metrics:
            if metric_name is None or metric_name == metric.get_name():
                print(f"I'm here: {metric.get_name()}")
                name = metric.get_name()
                measure_results = metric.get_measure_results()
                if measure_results is not None:
                    pivot_results[name] = measure_results
        return pivot_results
