from ..interface_routers.kpi_router_interface import KPIRouterInterface
from ..router_result import Result


def not_implemented():
    print("This has not been implemented")
    return Result(status=Result.Status.NOT_IMPLEMENTED,
                  message="Stub response: Not been implemented")


class KPIRouterStub(KPIRouterInterface):
    def on_get_kpi_names(self) -> Result:
        return not_implemented()

    def on_get_kpi_result(self, kpi_name=None) -> Result:
        return not_implemented()
