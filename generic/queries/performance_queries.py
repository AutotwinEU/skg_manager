from promg import Query

from performance_library.ecdf_library import EcdfConformanceMetrics


class PerformanceQueryLibrary:
    # =========================================================================================
    # removes all the performance_library nodes. used before adding performance_library to SKG.
    @staticmethod
    def delete_all_performance_nodes():
        # language=sql
        query_str = '''
            MATCH (c:Performance)
            DETACH DELETE c'''
        return Query(query_str=query_str)

    # =========================================================================================
    # creates all the high-level performance_library nodes
    # retrieves a lists with input sensors and corresponding output sensor(s)
    @staticmethod
    def retrieve_sensor_connections():
        query_str = '''
            MATCH (s1:Sensor {simulated:True}) 
            MATCH (s1) -[:ORIGIN] -> (:Connection) - [:DESTINATION] ->(s2)
            WHERE s1.sysId <> s2.sysId
            WITH s1, s2
            ORDER BY s2.sysId
            RETURN s1.sysId AS input, COLLECT(DISTINCT s2.sysId) AS outputs
            ORDER BY input
        '''
        return Query(query_str=query_str)

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
    # retrieves for a sensor, all the execution times on which activity takes place
    @staticmethod
    def timestamps_for_a_sensor(sensor):
        query_str = '''
            MATCH path=(ev:Event)-[:DF_CONTROL_FLOW_ITEM*]->(g:Event)
            WHERE NOT EXISTS((:Event)-[:DF_CONTROL_FLOW_ITEM]->(ev))
            AND NOT EXISTS((g)-[:DF_CONTROL_FLOW_ITEM]->(:Event))
            UNWIND nodes(path) as e
            MATCH (e)-[:EXECUTED_BY]->(s:Sensor)
            WHERE s.sysId="$sensor"
            WITH COLLECT(e.timestamp) as times
            RETURN times
                '''
        return Query(query_str=query_str,
                     template_string_parameters={"sensor": sensor}
                     )

    # =========================================================================================
    # # stores a performance_library artifact of a certain kind with a value in the database
    @staticmethod
    def store_ecfds_in_db(name, ecdfs, sensors):
        query_str = '''
            CREATE (parent:Performance:Latency {name: "$name"})
            WITH parent
            UNWIND $ecdfs as ecdf
            CALL {WITH parent, ecdf
                  CREATE (child:Performance:LatencyECDF 
                    {name: ecdf.legend, 
                    source: ecdf.gt_sim,
                    value: ecdf.serialized_ecdf,
                    min: ecdf.min,
                    max: ecdf.max,
                    average: ecdf.average,
                    median: ecdf.median
                    })
                  CREATE (parent) - [:HAS_PERFORMANCE] -> (child)
                  RETURN child
            }
            WITH child
            MATCH (s:Sensor)
            WHERE s.sysId IN $sensors AND ((child.source = "sim" AND s.simulated = true) OR (child.source = "gt" AND 
            s.simulated IS NULL))
            MERGE (s) - [:PERFORMED_BY] -> (child)
        '''
        return Query(query_str=query_str,
                     template_string_parameters={"name": name},
                     parameters={
                         "ecdfs": ecdfs,
                         "sensors": sensors
                     })

    @staticmethod
    def add_conformance_between_ecdfs(name1, name2, conformance: EcdfConformanceMetrics):
        query_str = '''
            MATCH (p1: LatencyECDF {name: $name1}) <- [:HAS_PERFORMANCE] - () - [:HAS_PERFORMANCE] -> (p2:LatencyECDF 
            {name: $name2})
            MERGE (p1) - [:CONFORMANCE {difference: $difference, similarity: $similarity, performance_library: 
            $performance_library, 
            kolmogorov: $kolmogorov}] -> (p2)'''
        return Query(query_str=query_str,
                     parameters={
                         "name1": name1,
                         "name2": name2,
                         "difference": conformance.difference,
                         "similarity": conformance.similarity,
                         "performance_library": conformance.performance,
                         "kolmogorov": conformance.kolmogorov
                     })

    # =========================================================================================
    @staticmethod
    def retrieve_all_ecdfs():
        query_str = '''
            MATCH (p:Latency) - [:HAS_PERFORMANCE] -> (n:LatencyECDF)
            RETURN p.name as title, collect(properties(n)) as ecdfs'''
        return Query(query_str=query_str)

    @staticmethod
    def similarity_difference_and_performance(ecdf_name1, ecdf_name2):
        query_str = '''match (e1:Performance:LatencyECDF{name:"$ecdf_name1"})
                       match (e2:Performance:LatencyECDF{name:"$ecdf_name2"})
                       match (e1)-[c:CONFORMANCE]->(e2)
                       return c.similarity as sim, c.difference as diff, c.performance_library as perf, c.kolmogorov 
                       as kolm'''
        return Query(query_str=query_str,
                     template_string_parameters={"ecdf_name1": ecdf_name1, "ecdf_name2": ecdf_name2})

    @staticmethod
    def get_ecdf_properties(name):
        query_str = '''MATCH (p:LatencyECDF{name:"$name"}) 
                       RETURN p.max as max, p.min as min, p.average as average, p.median as median'''
        return Query(query_str=query_str,
                     template_string_parameters={"name": name})
