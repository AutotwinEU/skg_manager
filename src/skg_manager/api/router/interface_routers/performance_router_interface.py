from abc import ABC, abstractmethod

from promg import DatabaseConnection

from ..router_result import Result


class PerformanceRouterInterface(ABC):

    @abstractmethod
    def on_calculate_performance(self, route_data) -> Result:
        pass

    @abstractmethod
    def on_retrieve_metrics(self, route_data) -> Result:
        pass

    @abstractmethod
    def on_get_ecdf_types(self) -> Result:
        pass

    @abstractmethod
    def on_get_metric_names(self, route_data) -> Result:
        pass
