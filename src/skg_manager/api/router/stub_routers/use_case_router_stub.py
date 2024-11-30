from ..interface_routers.use_case_router_interface import UseCaseRouterInterface
from ..router_result import Result


def not_implemented():
    print("This has not been implemented")


class UseCaseRouterStub(UseCaseRouterInterface):
    def on_get_use_case_name(self) -> Result:
        not_implemented()
        return Result(status=Result.Status.NOT_IMPLEMENTED, message="")

    def on_get_namespaces(self) -> Result:
        not_implemented()
        return Result(status=Result.Status.NOT_IMPLEMENTED, message="")

    def on_get_entity_types(self) -> Result:
        not_implemented()
        return Result(status=Result.Status.NOT_IMPLEMENTED, message="")
