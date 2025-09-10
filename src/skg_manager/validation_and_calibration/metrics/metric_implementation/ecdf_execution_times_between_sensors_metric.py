from typing import List, Optional

from promg import Query

from ...measures.measure_interfaces import MeasureInterface
from ...measures.measure_implementations import (KolmogorovMeasure, MedianRatioMeasure, SimilarityMeasure,
                                                 WassersteinDistanceMeasure, AverageDifferenceMeasure,
                                                 MedianDifferenceMeasure, MinimumDifferenceMeasure,
                                                 MaximumDifferenceMeasure)
from ..metric_interfaces.ecdf_metric_interface import EcdfMetricInterface


def get_time_unit(_input: str, default: str = "seconds") -> str:
    # Map abbreviations to full names
    unit_map = {
        "s": "seconds",
        "sec": "seconds",
        "m": "minutes",
        "min": "minutes",
        "h": "hours",
        "hr": "hours",
        "d": "days",
    }
    valid_units = set(unit_map.values()).union(set(unit_map.keys()))
    _input = _input.strip().lower()

    if _input in valid_units:
        # Return the full name if it's an abbreviation
        # if not abbreviation, then return user_input as default value.
        return unit_map.get(_input, _input)
    else:
        print(f"Warning: '{_input}' is not a valid time unit. Using default: '{default}'.")
        return default


def get_conversion_factor(unit: str) -> float:
    conversion_factors = {
        "seconds": 1,
        "minutes": 60,
        "hours": 3600,
        "days": 86400
    }
    return conversion_factors.get(unit, 1)  # Default to seconds if unknown


class ExecutionTimesBetweenSensorsEcdfMetric(EcdfMetricInterface):
    def __init__(self, measures: Optional[List[MeasureInterface]] = None, time_unit: str = 'seconds'):
        self.time_unit = get_time_unit(_input=time_unit)
        name = f"Execution Times Between Sensors (in {self.time_unit})"
        if measures is None:
            measures = [KolmogorovMeasure(), MedianRatioMeasure(), SimilarityMeasure(),
                        WassersteinDistanceMeasure(), AverageDifferenceMeasure(), MedianDifferenceMeasure(),
                        MinimumDifferenceMeasure(), MaximumDifferenceMeasure()]
        super().__init__(name=name,
                         measures=measures)

    def extract_ecdf_query_function(self, start_time="1970-01-01 00:00:00", end_time="2970-01-01 23:59:59"):
        """
        Provide a Query object that finds a list of numerical values (samples) for which an ecdf can be created.
        The query should return the following information
        - key --> the ecdf describes the distribution of an object, the key is a unique description of this object
        which can be understood by humans
        - element_id --> the ecdf describes the distribution of an object, the element_id is id of the object in the skg
        - is_simulated_data --> the ecdf is retrieved for simulated data or ground truth data
        - entity_type --> the entity_type for which the distribution is calculated
        - dist_values --> the values of the ecdf (a list of numerical values)

        :param start_time: start time of interval formatted as "yyyy-MM-dd HH:mm:ss"
        :param end_time: end time of interval formatted as "yyyy-MM-dd HH:mm:ss"
        :return: Query object that finds a list of numerical values
        """
        conversion_factor = get_conversion_factor(self.time_unit)
        query_str = '''
            MATCH (e1:Event) - [r:DF_CONTROL_FLOW_ITEM] -> (e2)
            WHERE e1.simulated = True OR 
                (e1.timestamp >= datetime(apoc.date.convertFormat($start_time,"yyyy-MM-dd HH:mm:ss","ISO_DATE_TIME")) 
                AND e2.timestamp <= datetime(apoc.date.convertFormat($end_time,"yyyy-MM-dd HH:mm:ss","ISO_DATE_TIME"))) 
            MATCH (e1) - [:ACTS_ON] -> (k) - [:IS_OF_TYPE] -> (et)
            MATCH (e1)-[:EXECUTED_BY]->(s1:Sensor)
            MATCH (e2)-[:EXECUTED_BY]->(s2:Sensor)
            MATCH (s1)-->(connection:Connection)-->(s2)
            WITH elementId(connection) as element_id, s1.simulated is not null as is_simulated_data, s1.sysId as 
            input_sensor, s2.sysId as output_sensor, et.entityType as entity_type, 
            COLLECT(duration.inSeconds(e1.timestamp, e2.timestamp).seconds/$conversion_factor) as times
            RETURN element_id, entity_type, is_simulated_data, input_sensor+"-"+output_sensor+"-"+entity_type as key, 
            times as dist_values
            '''
        return Query(query_str=query_str,
                     parameters={
                         "start_time": start_time,
                         "end_time": end_time,
                         "conversion_factor": conversion_factor
                     })
