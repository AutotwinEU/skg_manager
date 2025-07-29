from abc import ABC, abstractmethod
from typing import Optional, Tuple


class ValidationAndCalibrationServiceInterface(ABC):
    @abstractmethod
    def render_validation_template(self) -> str:
        pass

    @abstractmethod
    def calculate_performance(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        pass

    @abstractmethod
    def retrieve_mean_of_measures(self, metric_name: Optional[str]):
        pass

    @abstractmethod
    def get_metric_names(self):
        pass

    @abstractmethod
    def get_measure_names(self, metric_name: Optional[str]):
        pass
