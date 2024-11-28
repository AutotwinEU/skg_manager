from api.router.interface_routers.oced_pg_router_interface import OcedPgRouterInterface
from api.router.router_result import Result


def not_implemented():
    print("This has not been implemented")
    return Result(status=Result.Status.NOT_IMPLEMENTED,
                  message="Stub response: Not been implemented")


class OcedPgRouterStub(OcedPgRouterInterface):
    def on_load_records(self, route_data) -> Result:
        return not_implemented()

    def on_transform_records(self, route_data) -> Result:
        return not_implemented()

    def on_delete_simulated_data(self, route_data) -> Result:
        return not_implemented()
