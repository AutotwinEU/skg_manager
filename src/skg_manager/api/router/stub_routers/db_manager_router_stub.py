from ..interface_routers.db_manager_router_interface import DatabaseManagerRouterInterface
from ..router_result import Result


def not_implemented():
    print("This has not been implemented")
    return Result(status=Result.Status.NOT_IMPLEMENTED,
                  message="Stub response: Not been implemented")


class DatabaseManagerRouterStub(DatabaseManagerRouterInterface):

    def on_clear_db(self) -> Result:
        return not_implemented()

    def on_get_statistics(self) -> Result:
        return not_implemented()

    def on_get_timespan(self) -> Result:
        return not_implemented()

    def on_get_records_timespan(self) -> Result:
        return not_implemented()

    def on_get_logs(self) -> Result:
        return not_implemented()

    def on_get_event_log(self, entity_type) -> Result:
        return not_implemented()

    def on_get_model_ids(self) -> Result:
        return not_implemented()
