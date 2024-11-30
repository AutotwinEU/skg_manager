from ..interface_routers.performance_router_interface import PerformanceRouterInterface
from ..router_result import Result


class PerformanceRouter(PerformanceRouterInterface):
    def __init__(self, performance_module):
        self.performance_module = performance_module

    def on_calculate_performance(self) -> Result:
        try:
            self.performance_module.remove_performance_artifacts()
            self.performance_module.create_ecdf_collections()
            self.performance_module.add_ecdf_collection_to_skg()

            self.performance_module.create_aggregated_performance_html()
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully created performance_library metrics available at "
                                  "http://localhost:63342/skg_croma/docker/volumes/perfres/index.html")
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))
