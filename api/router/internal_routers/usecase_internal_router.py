from flask import Blueprint, make_response, Response

from api.exceptions.exception_handler import db_exception_handler
from api.router.interface_routers.use_case_router_interface import UseCaseRouterInterface
from api.router.router_result_converter import convert_result_into_response


class StatusInternalRouter:
    use_case_routes = Blueprint("use_case", __name__)

    def __init__(self, use_case_implementation: UseCaseRouterInterface):
        self.implementation = use_case_implementation
        self.use_case_routes.add_url_rule('/', 'handle_test_server',
                                          view_func=StatusInternalRouter.handle_test_server)
        self.use_case_routes.add_url_rule('/use_case', 'handle_get_use_case', view_func=self.handle_get_use_case)
        self.use_case_routes.add_url_rule('/namespaces', 'handle_get_namespaces',
                                          view_func=self.handle_get_namespaces)
        self.use_case_routes.add_url_rule('/entity_types', 'handle_get_entity_types',
                                          view_func=self.handle_get_entity_types)

    @staticmethod
    def handle_test_server() -> Response:
        return make_response(
            'Server is up and running!',
            200
        )

    @db_exception_handler
    def handle_get_use_case(self) -> Response:
        result = self.implementation.on_get_use_case_name()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_namespaces(self) -> Response:
        result = self.implementation.on_get_namespaces()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_entity_types(self) -> Response:
        result = self.implementation.on_get_entity_types()
        return convert_result_into_response(result)
