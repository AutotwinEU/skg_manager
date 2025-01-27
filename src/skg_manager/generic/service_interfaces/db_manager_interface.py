from abc import ABC, abstractmethod


class DatabaseManagerInterface(ABC):
    @abstractmethod
    def clear_db(self, replace):
        pass

    @abstractmethod
    def set_constraints(self, entity_key_name):
        pass

    @abstractmethod
    def get_constraints(self):
        pass

    @abstractmethod
    def get_statistics(self):
        pass

    @abstractmethod
    def get_timespan(self):
        pass

    @abstractmethod
    def get_ground_truth_records_time_span(self):
        pass

    @abstractmethod
    def get_imported_logs(self):
        pass

    @abstractmethod
    def test_connection(self) -> None:
        pass

    @abstractmethod
    def get_model_ids(self):
        pass

    @abstractmethod
    def get_station_ids(self, station_types):
        pass

    @abstractmethod
    def get_event_log(self, entity_type):
        pass
