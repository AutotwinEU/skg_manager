from abc import ABC, abstractmethod

from ..router_result import Result


class PerformanceRouterInterface(ABC):
    @abstractmethod
    def on_calculate_performance(self) -> Result:
        pass
