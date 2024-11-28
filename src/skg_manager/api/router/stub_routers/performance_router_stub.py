from ...router.interface_routers.performance_router_interface import PerformanceRouterInterface
from skg_manager import Result


def not_implemented():
    print("This has not been implemented")
    return Result(status=Result.Status.NOT_IMPLEMENTED,
                  message="Stub response: Not been implemented")


class PerformanceRouterStub(PerformanceRouterInterface):
    def on_calculate_performance(self) -> Result:
        return not_implemented()
