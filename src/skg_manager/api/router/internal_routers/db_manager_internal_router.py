from flask import Blueprint, make_response, Response

from src.skg_manager.api.exceptions.exception_handler import db_exception_handler
from src.skg_manager.api.router.interface_routers.db_manager_router_interface import DatabaseManagerRouterInterface
from src.skg_manager.api.router.router_result_converter import convert_result_into_response


class DatabaseManagerInternalRouter:
    db_manager_routes = Blueprint("db_manager", __name__, url_prefix="/db_manager")

    def __init__(self, implementation: DatabaseManagerRouterInterface):
        self.implementation = implementation
        self.db_manager_routes.add_url_rule('/test_response', 'handle_test_response',
                                            view_func=DatabaseManagerInternalRouter.handle_test_response)
        self.db_manager_routes.add_url_rule('/test_connection', 'handle_test_connection',
                                            view_func=self.handle_test_connection)
        self.db_manager_routes.add_url_rule('/clear_db', 'handle_clear_db', view_func=self.handle_clear_db,
                                            methods=['GET', 'POST'])
        self.db_manager_routes.add_url_rule('/statistics', 'handle_get_statistics',
                                            view_func=self.handle_get_statistics,
                                            methods=['GET'])
        self.db_manager_routes.add_url_rule('/time_span', 'handle_get_timespan', view_func=self.handle_get_timespan,
                                            methods=['GET'])
        self.db_manager_routes.add_url_rule('/records_time_span', 'handle_get_records_timespan',
                                            view_func=self.handle_get_records_timespan,
                                            methods=['GET'])
        self.db_manager_routes.add_url_rule('/logs', 'handle_get_logs', view_func=self.handle_get_logs,
                                            methods=['GET'])
        self.db_manager_routes.add_url_rule('/eventlog/<entity_type>', 'handle_get_event_log',
                                            view_func=self.handle_get_event_log,
                                            methods=['GET'])
        self.db_manager_routes.add_url_rule('/get_model_ids', 'handle_get_model_ids',
                                            view_func=self.handle_get_model_ids,
                                            methods=['GET'])

    @staticmethod
    def handle_test_response() -> Response:
        return make_response(
            'Test worked!',
            200
        )

    @db_exception_handler
    def handle_test_connection(self) -> Response:
        result = self.implementation.on_test_connection()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_clear_db(self) -> Response:
        result = self.implementation.on_clear_db()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_statistics(self) -> Response:
        result = self.implementation.on_get_statistics()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_timespan(self) -> Response:
        result = self.implementation.on_get_timespan()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_records_timespan(self) -> Response:
        result = self.implementation.on_get_records_timespan()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_logs(self) -> Response:
        result = self.implementation.on_get_logs()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_event_log(self, entity_type) -> Response:
        result = self.implementation.on_get_event_log(entity_type)
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_model_ids(self) -> Response:
        result = self.implementation.on_get_model_ids()
        return convert_result_into_response(result)
