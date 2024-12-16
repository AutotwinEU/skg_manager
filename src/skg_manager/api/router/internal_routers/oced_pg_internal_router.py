from flask import Blueprint, request, Response

from ..interface_routers.oced_pg_router_interface import OcedPgRouterInterface
from ...exceptions.exception_handler import db_exception_handler
from ..router_result_converter import convert_result_into_response


class OcedPgInternalRouter:
    oced_pg_routes = Blueprint("ocedpg", __name__, url_prefix="/oced_pg")

    def __init__(self, implementation: OcedPgRouterInterface):
        self.implementation = implementation
        self.oced_pg_routes.add_url_rule('/load', 'handle_load_records', view_func=self.handle_load_records,
                                         methods=['POST'])
        self.oced_pg_routes.add_url_rule('/transform', 'handle_transform_records',
                                         view_func=self.handle_transform_records,
                                         methods=['POST'])
        self.oced_pg_routes.add_url_rule('/delete_simulated_data', 'handle_delete_simulated_data',
                                         view_func=self.handle_delete_simulated_data,
                                         methods=['POST'])

    @db_exception_handler
    def handle_load_records(self) -> Exception | Response:
        route_data = request.args
        try:
            result = self.implementation.on_load_records(route_data)
        except Exception as e:
            return e
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_transform_records(self) -> Response:
        route_data = request.args
        result = self.implementation.on_transform_records(route_data)
        return convert_result_into_response(result)

    @db_exception_handler
    def handle_delete_simulated_data(self) -> Response:
        route_data = request.args
        result = self.implementation.on_delete_simulated_data(route_data)
        return convert_result_into_response(result)
