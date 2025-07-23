from flask import Blueprint, Response, request, send_from_directory, render_template, send_file

from ...exceptions.exception_handler import db_exception_handler
from ..interface_routers.performance_router_interface import PerformanceRouterInterface
from ..router_result_converter import convert_result_into_response


class PerformanceInternalRouter:
    performance_routes = Blueprint("performance", __name__, url_prefix="/performance")

    def __init__(self, implementation: PerformanceRouterInterface):
        self.implementation = implementation
        self.performance_routes.add_url_rule("/run", "handle_calculate_performance",
                                             view_func=self.handle_calculate_performance,
                                             methods=["POST"])
        self.performance_routes.add_url_rule("/get_mean", "handle_retrieve_mean",
                                             view_func=self.handle_retrieve_mean,
                                             methods=["GET"])
        self.performance_routes.add_url_rule("/get_ecdf_types", "handle_get_ecdf_types",
                                             view_func=self.handle_get_ecdf_types,
                                             methods=["GET"])
        self.performance_routes.add_url_rule("/get_measure_names", "handle_get_measure_names",
                                             view_func=self.handle_get_measure_names,
                                             methods=["GET"])
        self.performance_routes.add_url_rule("/show_results", "show_results",
                                             view_func=self.show_results, methods=["GET"])

    @db_exception_handler
    def handle_calculate_performance(self) -> Response:
        route_data = request.args
        result = self.implementation.on_calculate_performance(route_data)
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_retrieve_mean(self) -> Response:
        route_data = request.args
        result = self.implementation.on_retrieve_mean(route_data)
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_ecdf_types(self) -> Response:
        result = self.implementation.on_get_ecdf_types()
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_get_measure_names(self) -> Response:
        route_data = request.args
        result = self.implementation.on_get_measure_names(route_data)
        return convert_result_into_response(result)

    def show_results(self) -> str:
        return self.implementation.on_show_results()
