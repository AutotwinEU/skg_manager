from flask import Blueprint, Response

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

    @db_exception_handler
    def handle_calculate_performance(self) -> Response:
        result = self.implementation.on_calculate_performance()
        return convert_result_into_response(result)
