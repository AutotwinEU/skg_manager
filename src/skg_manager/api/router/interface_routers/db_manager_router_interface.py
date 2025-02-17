from abc import ABC, abstractmethod

from ..router_result import Result


class DatabaseManagerRouterInterface(ABC):
    @abstractmethod
    def on_clear_db(self) -> Result:
        pass

    @abstractmethod
    def on_get_statistics(self) -> Result:
        pass

    @abstractmethod
    def on_get_timespan(self) -> Result:
        pass

    @abstractmethod
    def on_get_ground_truth_records_timespan(self) -> Result:
        pass

    @abstractmethod
    def on_get_logs(self) -> Result:
        pass

    @abstractmethod
    def on_get_event_log(self, entity_type) -> Result:
        pass

    @abstractmethod
    def on_get_model_ids(self) -> Result:
        pass

    @abstractmethod
    def on_get_station_ids(self, route_data = None) -> Result:
        pass

    @abstractmethod
    def on_test_connection(self) -> Result:
        pass
