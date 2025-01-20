from abc import ABC, abstractmethod


class EcdfMetricCalculatorInterface(ABC):
    @abstractmethod
    def remove_ecdfs_from_skg(self):
        pass

    @abstractmethod
    def calculate_ecdfs_from_skg(self):
        pass

    @abstractmethod
    def add_ecdfs_to_skg(self):
        pass

    @abstractmethod
    def create_aggregated_performance_html(self):
        pass
