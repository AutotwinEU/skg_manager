from ...router.interface_routers.performance_router_interface import PerformanceRouterInterface
from ..router_result import Result


def not_implemented():
    print("This has not been implemented")
    return Result(status=Result.Status.NOT_IMPLEMENTED,
                  message="Stub response: Not been implemented")


class PerformanceRouterStub(PerformanceRouterInterface):

    def on_calculate_performance(self, route_data) -> Result:
        return not_implemented()

    def on_retrieve_metrics(self, route_data) -> Result:
        return not_implemented()

    def on_get_ecdf_types(self) -> Result:
        return not_implemented()

    def on_get_metric_names(self, route_data) -> Result:
        return not_implemented()
