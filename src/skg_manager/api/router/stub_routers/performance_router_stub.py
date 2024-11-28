from src.skg_manager.api.router.interface_routers.performance_router_interface import PerformanceRouterInterface
from src.skg_manager.api.router.router_result import Result


def not_implemented():
    print("This has not been implemented")
    return Result(status=Result.Status.NOT_IMPLEMENTED,
                  message="Stub response: Not been implemented")


class PerformanceRouterStub(PerformanceRouterInterface):
    def on_calculate_performance(self) -> Result:
        return not_implemented()
