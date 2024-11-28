from abc import ABC, abstractmethod

from skg_manager import Result


class PerformanceRouterInterface(ABC):
    @abstractmethod
    def on_calculate_performance(self) -> Result:
        pass
