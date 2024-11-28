from ....api.router.interface_routers.oced_pg_router_interface import OcedPgRouterInterface
from ....api.router.route_data_extractors import extract_is_simulation_data
from ....api.router.router_result import Result


class ConditionalOcedPGRouter(OcedPgRouterInterface):
    def __init__(self, ground_truth_router: OcedPgRouterInterface,
                 simulation_router: OcedPgRouterInterface):
        self.ground_truth_router = ground_truth_router
        self.simulation_router = simulation_router

    def on_load_records(self, route_data) -> Result:
        if extract_is_simulation_data(route_data):
            return self.simulation_router.on_load_records(route_data)
        else:
            return self.ground_truth_router.on_load_records(route_data)

    def on_transform_records(self, route_data) -> Result:
        if extract_is_simulation_data(route_data):
            return self.simulation_router.on_transform_records(route_data)
        else:
            return self.ground_truth_router.on_transform_records(route_data)

    def on_delete_simulated_data(self, route_data) -> Result:
        if extract_is_simulation_data(route_data):
            return self.simulation_router.on_delete_simulated_data(route_data)
        else:
            return self.ground_truth_router.on_delete_simulated_data(route_data)
