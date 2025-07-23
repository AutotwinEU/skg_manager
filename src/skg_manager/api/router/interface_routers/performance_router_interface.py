from abc import ABC, abstractmethod
from typing import Tuple

from promg import DatabaseConnection

from ..router_result import Result


class PerformanceRouterInterface(ABC):

    @abstractmethod
    def on_show_results(self) -> str:
        pass

    @abstractmethod
    def on_retrieve_mean(self, route_data) -> Result:
        pass

    @abstractmethod
    def on_get_ecdf_types(self) -> Result:
        pass

    @abstractmethod
    def on_get_measure_names(self, route_data) -> Result:
        pass
