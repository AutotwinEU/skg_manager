from abc import ABC, abstractmethod


class MetricInterface(ABC):
    @abstractmethod
    def calculate(self, gt_dist, sim_dist):
        pass

    @abstractmethod
    def get_name(self):
        pass
