from promg import Query

from skg_manager.validation_and_calibration.vc_service_interfaces.ecdf_service_interface import EcdfServiceInterface


class ExecutionTimesBetweenSensorsEcdfHandler(EcdfServiceInterface):
    def __init__(self):
        super().__init__(described_behavior="Execution Times Between Sensors")

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

        query_str = '''
            MATCH (e1:Event) - [r:DF_CONTROL_FLOW_ITEM] -> (e2)
            WHERE e1.timestamp >= datetime(apoc.date.convertFormat($start_time,"yyyy-MM-dd HH:mm:ss","ISO_DATE_TIME")) 
            AND e2.timestamp <= datetime(apoc.date.convertFormat($end_time,"yyyy-MM-dd HH:mm:ss","ISO_DATE_TIME")) 
            MATCH (e1) - [:ACTS_ON] -> (k) - [:IS_OF_TYPE] -> (et)
            MATCH (e1)-[:EXECUTED_BY]->(s1:Sensor)
            MATCH (e2)-[:EXECUTED_BY]->(s2:Sensor)
            MATCH (s1)-->(connection:Connection)-->(s2)
            WITH elementId(connection) as element_id, s1.simulated is not null as is_simulated_data, s1.sysId as 
            input_sensor, s2.sysId as output_sensor, et.entityType as entity_type, 
            COLLECT(duration.inSeconds(e1.timestamp, e2.timestamp).seconds) as times
            RETURN element_id, entity_type, is_simulated_data, input_sensor+"-"+output_sensor+"-"+entity_type as key, 
            times as dist_values
            '''
        return Query(query_str=query_str,
                     parameters={
                         "start_time": start_time,
                         "end_time": end_time
                     })
