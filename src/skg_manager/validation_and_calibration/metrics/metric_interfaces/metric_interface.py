from abc import abstractmethod, ABC
from typing import List

from promg import DatabaseConnection

from ...measures.measure_interfaces import MeasureInterface


class MetricInterface(ABC):
    def __init__(self, name: str, measures: List[MeasureInterface]):
        self.name = name
        self.measures = measures
        self.result = None
        self.html_content = None
        self.db_connection = None

    ####################
    # Abstract Methods #
    ####################
    @abstractmethod
    def clear_result(self):
        pass

    @abstractmethod
    def calculate_result(self, start_time=None, end_time=None):
        pass

    @abstractmethod
    def generate_html_content(self):
        pass

    #######################
    # Implemented Methods #
    #######################

    def set_db_connection(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def check_db_connection(self):
        if self.db_connection is None:
            return False
        return True

    def get_name(self):
        return self.name

    def get_html_content(self):
        if self.html_content is None:
            self.generate_html_content()
        return self.html_content

    def get_dict_repr(self):
        return {
            'name': self.get_name(),
            'content': self.get_html_content()
        }

    def get_measures(self):
        result = []
        for measure in self.measures:
            measure = {
                "name": measure.get_name(),
                "optimization_type": measure.get_optimization_direction(),
            }
            result.append(measure)
        return result
