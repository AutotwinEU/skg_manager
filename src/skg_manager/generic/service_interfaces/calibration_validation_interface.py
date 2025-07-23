from abc import ABC, abstractmethod
from typing import Optional, Tuple


class ValidationAndCalibrationServiceInterface(ABC):
    @abstractmethod
    def render_validation_template(self):
        pass

    @abstractmethod
    def calculate_performance(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        pass

    @abstractmethod
    def retrieve_mean(self, ecdf_type: Optional[str]):
        pass

    @abstractmethod
    def get_ecdf_types(self):
        pass

    @abstractmethod
    def get_measure_names(self, ecdf_type: Optional[str]):
        pass
