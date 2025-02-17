from abc import ABC, abstractmethod

from ..router_result import Result


class OcedPgRouterInterface(ABC):
    @abstractmethod
    def on_load_records(self, route_data) -> Result:
        pass

    @abstractmethod
    def on_transform_records(self, route_data) -> Result:
        pass

    @abstractmethod
    def on_clean_transformed_data(self, route_data) -> Result:
        pass

    @abstractmethod
    def on_delete_simulated_data(self, route_data) -> Result:
        pass
