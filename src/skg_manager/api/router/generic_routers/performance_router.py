from typing import List

from promg import DatabaseConnection

from ....generic.service_interfaces.calibration_validation_interface import ValidationAndCalibrationServiceInterface
from ....validation_and_calibration import EcdfWrapperInterface
from ..interface_routers.performance_router_interface import PerformanceRouterInterface
from ..router_result import Result


class PerformanceRouter(PerformanceRouterInterface):
    def __init__(self, validation_and_calibration_service: ValidationAndCalibrationServiceInterface):
        self.vc_service = validation_and_calibration_service

    def on_calculate_performance(self, route_data) -> Result:
        start_date = route_data['start_date'] if 'start_date' in route_data else None
        end_date = route_data['end_date'] if 'end_date' in route_data else None

        try:
            self.vc_service.calculate_performance(start_date, end_date)
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully created performance_library metrics available at "
                                  "http://localhost:63342/skg_croma/docker/volumes/perfres/index.html")
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_retrieve_metrics(self, route_data) -> Result:
        ecdf_type = route_data['ecdf_type'] if 'ecdf_type' in route_data else None
        try:
            result = self.vc_service.retrieve_mean_metrics(ecdf_type)
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully retrieved metrics",
                          data=result)
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_get_ecdf_types(self):
        try:
            result = self.vc_service.get_ecdf_types()
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully retrieved ecdf types",
                          data=result)

        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_get_metric_names(self, route_data):
        ecdf_type = route_data['ecdf_type'] if 'ecdf_type' in route_data else None

        try:
            result = self.vc_service.get_metric_names(ecdf_type=ecdf_type)
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully retrieved ecdf types",
                          data=result)

        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))
