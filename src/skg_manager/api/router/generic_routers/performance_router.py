from flask import Response

from ....generic.service_interfaces.calibration_validation_interface import ValidationAndCalibrationServiceInterface
from ..interface_routers.performance_router_interface import PerformanceRouterInterface
from ..router_result import Result


def to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower()
        if value in ("true", "yes", "1"):
            return True
        elif value in ("false", "no", "0"):
            return False
    raise ValueError(f"Cannot convert {value} to boolean")


class PerformanceRouter(PerformanceRouterInterface):
    def __init__(self, validation_and_calibration_service: ValidationAndCalibrationServiceInterface):
        self.vc_service = validation_and_calibration_service

    def on_show_results(self) -> str:
        return self.vc_service.render_validation_template()

    def on_calculate_performance(self, route_data) -> Result:
        start_date = route_data['start_date'] if 'start_date' in route_data else None
        end_date = route_data['end_date'] if 'end_date' in route_data else None
        # default is used for calibration
        used_for_calibration = to_bool(
            route_data['used_for_calibration']) if 'used_for_calibration' in route_data else True
        try:
            self.vc_service.calculate_performance(start_date, end_date, used_for_calibration)
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully created performance results")
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_retrieve_mean_of_measures(self, route_data) -> Result:
        metric_name = route_data['metric_name'] if 'metric_name' in route_data else None
        try:
            result = self.vc_service.retrieve_mean_of_measures(metric_name)
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully retrieved mean",
                          data=result)
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_get_metric_names(self):
        try:
            result = self.vc_service.get_metric_names()
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully retrieved metric names",
                          data=result)

        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_get_measure_names(self, route_data):
        metric_name = route_data['metric_name'] if 'metric_name' in route_data else None

        try:
            result = self.vc_service.get_measure_names(metric_name=metric_name)
            return Result(status=Result.Status.SUCCESS,
                          message="Successfully retrieved measures for metric names",
                          data=result)

        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))
