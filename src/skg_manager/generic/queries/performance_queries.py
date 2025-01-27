from typing import Dict, Any, Optional

from promg import Query


class PerformanceQueryLibrary:
    # =========================================================================================
    # removes all the performance_library nodes. used before adding performance_library to SKG.
    @staticmethod
    def delete_ecdf_nodes(_type: Optional[str] = None):
        if _type is None:
            # language=sql
            query_str = '''
                            MATCH (d:ECDF)
                            DETACH DELETE d'''
            return Query(query_str=query_str
                         )
        else:
            # language=sql
            query_str = '''
                            MATCH (d:ECDF {type:$type})
                            DETACH DELETE d'''
            return Query(query_str=query_str,
                         parameters={"type": _type}
                         )

    # =========================================================================================
    @staticmethod
    def execution_times_between_sensors():
        query_str = '''
            MATCH (e1:Event) - [r:DF_CONTROL_FLOW_ITEM] -> (e2)
            MATCH (e1)-[:EXECUTED_BY]->(s1:Sensor)
            MATCH (e2)-[:EXECUTED_BY]->(s2:Sensor)
            WITH s1.simulated is not null as is_simulated_data, s1.sysId as input_sensor, s2.sysId as output_sensor, 
            COLLECT(duration.inSeconds(e1.timestamp, e2.timestamp).seconds) as times
            RETURN is_simulated_data, input_sensor, output_sensor, times
            '''
        return Query(query_str=query_str)

    # =========================================================================================
    @staticmethod
    def retrieve_distributions(_type: Optional[str]):
        if _type is None:
            query_str = '''
                MATCH (n:ECDF)
                RETURN n.value as ecdf'''
            return Query(query_str=query_str)
        else:
            query_str = '''
                            MATCH (n:ECDF {type:$type})
                            RETURN n.value as ecdf'''
            return Query(query_str=query_str,
                         parameters={"type": _type})

    @staticmethod
    def similarity_difference_and_performance(ecdf_name1, ecdf_name2):
        query_str = '''match (e1:Performance:LatencyECDF{name:"$ecdf_name1"})
                       match (e2:Performance:LatencyECDF{name:"$ecdf_name2"})
                       match (e1)-[c:CONFORMANCE]->(e2)
                       return c.similarity as sim, c.difference as diff, c.performance as perf, c.kolmogorov 
                       as kolm'''
        return Query(query_str=query_str,
                     template_string_parameters={"ecdf_name1": ecdf_name1, "ecdf_name2": ecdf_name2})

    @staticmethod
    def get_ecdf_properties(name):
        query_str = '''MATCH (p:LatencyECDF{name:"$name"}) 
                       RETURN p.max as max, p.min as min, p.average as average, p.median as median'''
        return Query(query_str=query_str,
                     template_string_parameters={"name": name})

    @staticmethod
    def get_get_metrics_query(ecdf_type: Optional[str] = None):
        if ecdf_type is None:
            query_str = '''
                MATCH (n_gt:ECDF {source:"gt"}) - [metrics:COMPARES_TO] -> (n_sim:ECDF {source:"sim"})
                WITH n_gt.type as ecdf_type, properties(metrics) as conformance_metrics
                RETURN ecdf_type, collect(conformance_metrics) as metrics
            '''
        else:
            query_str = '''
                MATCH (n_gt:ECDF {source:"gt"}) - [metrics:COMPARES_TO] -> (n_sim:ECDF {source:"sim"})
                WHERE n_gt.type = $ecdf_type
                WITH n_gt.type as ecdf_type, properties(metrics) as conformance_metrics
                RETURN ecdf_type, collect(conformance_metrics) as metrics
            '''
        return Query(query_str=query_str,
                     parameters={"ecdf_type": ecdf_type})

    @staticmethod
    def get_get_ecdf_type_query():
        query_str = '''MATCH (n:ECDF)
                       RETURN collect(distinct n.type) as ecdf_types
        '''

        return Query(query_str=query_str)
