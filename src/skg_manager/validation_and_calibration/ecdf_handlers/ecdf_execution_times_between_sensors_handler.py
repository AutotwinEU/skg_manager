from promg import Query

from skg_manager.validation_and_calibration.vc_service_interfaces.graph_ecdf_handler_interface import GraphEcdfHandlerInterface


class ExecutionTimesBetweenSensorsEcdfHandler(GraphEcdfHandlerInterface):
    def __init__(self, db_connection):
        super().__init__(db_connection, type="Execution Times Between Sensors")

    def extract_ecdf_query_function(self, time_interval):
        query_str = '''
            MATCH (e1:Event) - [r:DF_CONTROL_FLOW_ITEM] -> (e2)
            MATCH (e1)-[:EXECUTED_BY]->(s1:Sensor)
            MATCH (e2)-[:EXECUTED_BY]->(s2:Sensor)
            MATCH (s1)-->(connection:Connection)-->(s2)
            WITH elementId(connection) as element_id, s1.simulated is not null as is_simulated_data, s1.sysId as 
            input_sensor, s2.sysId as output_sensor, 
            COLLECT(duration.inSeconds(e1.timestamp, e2.timestamp).seconds) as times
            RETURN element_id, is_simulated_data, input_sensor+"-"+output_sensor as key, times as dist_values
            '''
        return Query(query_str=query_str)
