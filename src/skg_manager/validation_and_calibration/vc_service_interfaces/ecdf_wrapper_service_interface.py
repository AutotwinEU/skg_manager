from abc import ABC, abstractmethod


class EcdfWrapperInterface(ABC):
    @abstractmethod
    def set_db_connection(self, db_connection):
        pass

    @abstractmethod
    def get_ecdf_type(self):
        pass

    @abstractmethod
    def get_metrics(self):
        pass

    @abstractmethod
    def remove_ecdfs_from_skg(self):
        pass

    @abstractmethod
    def calculate_ecdfs_from_skg(self):
        pass

    @abstractmethod
    def add_ecdfs_to_skg(self):
        pass

    @abstractmethod
    def create_aggregated_performance_html(self):
        pass
