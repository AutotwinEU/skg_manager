from abc import ABC, abstractmethod

from src.skg_manager.api.router.router_result import Result


class UseCaseRouterInterface(ABC):
    @abstractmethod
    def on_get_use_case_name(self) -> Result:
        pass

    @abstractmethod
    def on_get_namespaces(self) -> Result:
        pass

    @abstractmethod
    def on_get_entity_types(self) -> Result:
        pass
