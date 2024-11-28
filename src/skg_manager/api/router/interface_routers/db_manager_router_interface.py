from abc import ABC, abstractmethod

from skg_manager import Result


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
    def on_get_records_timespan(self) -> Result:
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
    def on_test_connection(self) -> Result:
        pass
