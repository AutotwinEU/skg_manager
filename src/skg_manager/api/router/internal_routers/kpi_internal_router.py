from flask import Blueprint, make_response, Response, request

from ....api.exceptions.exception_handler import db_exception_handler
from ...router.interface_routers.kpi_router_interface import KPIRouterInterface
from ...router.router_result_converter import convert_result_into_response


class KPIInternalRouter:
    kpi_routes = Blueprint("kpi", __name__, url_prefix="/kpi")

    def __init__(self, implementation: KPIRouterInterface):
        self.implementation = implementation
        self.kpi_routes.add_url_rule('/test_response', 'handle_test_response',
                                     view_func=KPIInternalRouter.handle_test_response)
        self.kpi_routes.add_url_rule('/names', 'get_kpi_names',
                                     view_func=self.get_kpi_names,
                                     methods=['GET'])
        self.kpi_routes.add_url_rule('/<kpi_name>', 'get_kpi_result',
                                     view_func=self.get_kpi_result,
                                     methods=['GET'])
        self.kpi_routes.add_url_rule('/results', 'get_all_kpi_results',
                                     view_func=self.get_all_kpi_results,
                                     methods=['GET'])

    @staticmethod
    def handle_test_response() -> Response:
        return make_response(
            'Test worked!',
            200
        )

    @db_exception_handler
    def get_kpi_names(self) -> Response:
        result = self.implementation.on_get_kpi_names()
        return convert_result_into_response(result)

    @db_exception_handler
    def get_kpi_result(self, kpi_name) -> Response:
        route_data = request.args
        entity_types = [route_data["entityType"]] if "entityType" in route_data else None
        result = self.implementation.on_get_kpi_result(kpi_name=kpi_name, entity_types=entity_types)
        return convert_result_into_response(result)

    @db_exception_handler
    def get_all_kpi_results(self) -> Response:
        route_data = request.args
        entity_types = [route_data["entityType"]] if "entityType" in route_data else None
        result = self.implementation.on_get_kpi_result(kpi_name=None, entity_types=entity_types)
        return convert_result_into_response(result)
