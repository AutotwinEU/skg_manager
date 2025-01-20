from typing import List

from ....validation_and_calibration import EcdfMetricCalculatorInterface
from ..interface_routers.performance_router_interface import PerformanceRouterInterface
from ..router_result import Result


class PerformanceRouter(PerformanceRouterInterface):
    def __init__(self, ecdf_metric_calculators: List[EcdfMetricCalculatorInterface]):
        self.ecdf_services = ecdf_metric_calculators

    def on_calculate_performance(self, remove_previous_results=True) -> Result:
        for ecdf_service in self.ecdf_services:
            try:
                if remove_previous_results:
                    ecdf_service.remove_ecdfs_from_skg()
                ecdf_service.calculate_ecdfs_from_skg()
                ecdf_service.add_ecdfs_to_skg()
                ecdf_service.create_aggregated_performance_html()
            except Exception as e:
                return Result(status=Result.Status.FAILURE, message=str(e))
        return Result(status=Result.Status.SUCCESS,
                      message="Successfully created performance_library metrics available at "
                              "http://localhost:63342/skg_croma/docker/volumes/perfres/index.html")
