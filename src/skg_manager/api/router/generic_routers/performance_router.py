from typing import List

from ....validation_and_calibration import EcdfWrapperInterface
from ..interface_routers.performance_router_interface import PerformanceRouterInterface
from ..router_result import Result


class PerformanceRouter(PerformanceRouterInterface):
    def __init__(self, ecdf_wrappers: List[EcdfWrapperInterface]):
        self.ecdf_wrappers = ecdf_wrappers

    def on_calculate_performance(self, remove_previous_results=True) -> Result:
        for exdf_wrapper in self.ecdf_wrappers:
            try:
                if remove_previous_results:
                    exdf_wrapper.remove_ecdfs_from_skg()
                exdf_wrapper.calculate_ecdfs_from_skg()
                exdf_wrapper.add_ecdfs_to_skg()
                exdf_wrapper.create_aggregated_performance_html()
            except Exception as e:
                return Result(status=Result.Status.FAILURE, message=str(e))
        return Result(status=Result.Status.SUCCESS,
                      message="Successfully created performance_library metrics available at "
                              "http://localhost:63342/skg_croma/docker/volumes/perfres/index.html")
