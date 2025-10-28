from abc import abstractmethod, ABC
from typing import List

from promg import DatabaseConnection

from ...measures.measure_interfaces import MeasureInterface


class MetricInterface(ABC):
    def __init__(self, name: str, measures: List[MeasureInterface], used_for_calibration=False):
        self.name = name
        self.measures = measures
        self.result = None
        self.html_content = None
        self.db_connection = None
        self.used_for_calibration = used_for_calibration

    ####################
    # Abstract Methods #
    ####################
    @abstractmethod
    def calculate_result(self, start_time, end_time):
        pass

    @abstractmethod
    def generate_html_content(self):
        pass

    #######################
    # Implemented Methods #
    #######################
    def has_result(self):
        return self.result is not None

    def clear_result(self):
        self.result = None

    def set_db_connection(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def check_db_connection(self):
        if self.db_connection is None:
            return False
        return True

    def get_name(self):
        return self.name

    def get_html_content(self):
        if self.result is None:
            return (f"No results has been generated for metric {self.name}. <br><br> "
                    f"Try to generate results using one of the following options"
                    f"<ul> <li>by pressing <span style='color: #ff804b'>Generate twin performance statistics</span> in the Orchestrator </li>"
                    f"<li> by running <span style='color: #ff804b'>/performance/run</span> via the swagger of the SKG manager.</li></ul>")
        self.generate_html_content()
        return self.html_content

    def get_dict_repr(self):
        return {
            'name': self.get_name(),
            'content': self.get_html_content()
        }

    def get_measures(self):
        result = []
        if self.measures is None:
            return []
        for measure in self.measures:
            measure = {
                "name": measure.get_name(),
                "optimization_type": measure.get_optimization_direction(),
            }
            result.append(measure)
        return result

    def get_measure_results(self):
        if self.measures is None:
            return None
        assert hasattr(self, '_get_measure_results') and callable(self._get_measure_results), \
            "_get_measure_results must be implemented when measures is defined"
        return self._get_measure_results()

    def _get_measure_results(self):
        raise NotImplementedError
