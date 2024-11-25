from abc import ABC, abstractmethod


class ModuleInterface(ABC):
    @abstractmethod
    def hello_world(self):
        print("hello world")