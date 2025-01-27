from abc import ABC, abstractmethod


class CalibrationServiceInterface(ABC):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    @abstractmethod
    def on_evaluate_metrics(self, ecdf_type):
        pass
