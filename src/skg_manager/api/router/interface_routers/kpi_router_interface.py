from abc import ABC, abstractmethod
from typing import Optional, List

from ..router_result import Result


class KPIRouterInterface(ABC):
    @abstractmethod
    def on_get_kpi_names(self) -> Result:
        pass

    @abstractmethod
    def on_get_kpi_result(self, kpi_name: Optional[str] = None,
                          entity_types: Optional[List[str]] = None) -> Result:
        pass
