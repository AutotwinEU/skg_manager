from abc import ABC, abstractmethod
from typing import Optional


class MethodCreator(ABC):
    """
        The Creator class declares the factory method that is supposed to return an
        object of a Product class. The Creator's subclasses usually provide the
        implementation of this method.
    """

    @abstractmethod
    def factory_method(self, config, is_simulation_data: Optional[bool] = None):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        pass

    def some_operation(self) -> str:
        """
        Also note that, despite its name, the Creator's primary responsibility
        is not creating products. Usually, it contains some core business logic
        that relies on Product objects, returned by the factory method.
        Subclasses can indirectly change that business logic by overriding the
        factory method and returning a different type of product from it.
        """

        # Call the factory method to create a Product object.
        product = self.factory_method()

        # Now, use the product.
        result = f"Creator: The same creator's code has just worked with {product.operation()}"

        return result


class Methods(ABC):
    @abstractmethod
    def get_defined_file_names(self):
        pass

    @abstractmethod
    def preprocess_files(self):
        pass

    @abstractmethod
    def clear_db(self):
        pass

    @abstractmethod
    def get_imported_logs(self):
        pass

    @abstractmethod
    def get_model_ids(self):
        pass

    @abstractmethod
    def get_event_log(self, entity_type):
        pass

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def filter_record_layer(self, entity_types, start_date, end_date):
        pass

    @abstractmethod
    def delete_data(self, logs=None):
        pass

    @abstractmethod
    def transform_data(self):
        pass

    @abstractmethod
    def get_statistics(self):
        pass

    @abstractmethod
    def get_timespan(self):
        pass

    @abstractmethod
    def get_records_timespan(self):
        pass

    @abstractmethod
    def add_performance_metrics(self):
        pass
