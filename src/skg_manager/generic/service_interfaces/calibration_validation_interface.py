from abc import ABC, abstractmethod
from typing import Optional


class ValidationAndCalibrationServiceInterface(ABC):
    @abstractmethod
    def calculate_performance(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        pass

    @abstractmethod
    def retrieve_mean_metrics(self, ecdf_type: Optional[str]):
        pass

    @abstractmethod
    def get_ecdf_types(self):
        pass

    @abstractmethod
    def get_metric_names(self, ecdf_type: Optional[str]):
        pass
