from abc import ABC, abstractmethod
from typing import Optional


class ValidationAndCalibrationServiceInterface(ABC):
    @abstractmethod
    def calculate_performance(self, remove_previous_results):
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
