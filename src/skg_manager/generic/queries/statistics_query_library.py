from promg import Query


class StatisticsQueryLibrary:
    @staticmethod
    def get_record_layer_statistics():
        query_str = '''
            MATCH (l:Log) - [:CONTAINS] -> (r:Record)
            WITH l.name as log, count(r) as numberOfNodes, CASE 
            WHEN l.name CONTAINS "sim" THEN TRUE
            ELSE FALSE
            END AS is_simulated
            RETURN log, is_simulated, numberOfNodes ORDER BY log
        '''

        return Query(query_str=query_str)

    @staticmethod
    def get_time_span_of_ground_truth_records_query():
        query_str = '''
            MATCH (l:Log) - [:CONTAINS] -> (r:Record)
            WHERE NOT l.name CONTAINS "sim"
            WITH min(r.timestamp) as start_time, max(r.timestamp) as end_time
            WITH date(start_time) as start_date, date(end_time) as end_date
            RETURN toString(start_date) as start_date, toString(end_date) as end_date
        '''

        return Query(query_str=query_str)

    @staticmethod
    def get_time_span_query():
        query_str = '''
            MATCH (e:Event) - [:EXECUTED_BY] -> (s:Sensor)
            WITH s.sysId as sensorId, min(e.timestamp) as start_time, max(e.timestamp) as end_time order by sensorId
            WITH date(max(start_time)) as start_date, date(min(end_time)) as end_date
            WITH datetime({year:start_date.year, month:start_date.month, day:start_date.day, hour:0, minute:0, 
            second:0}) as start_datetime,
            datetime({year:end_date.year, month:end_date.month, day:end_date.day, hour:23, minute:59, second:59}) as 
            end_datetime
            RETURN toString(start_datetime) as start_date, toString(end_datetime) as end_date
        '''

        return Query(query_str=query_str)

    @staticmethod
    def get_node_count_query() -> Query:
        # language=SQL
        query_str = '''
                    // List all node types and counts
                    MATCH (n) 
                    WHERE not "Record" in labels(n)
                    WITH  labels(n) AS labels,  count(n) AS numberOfNodes, CASE
                    WHEN n.simulated THEN TRUE
                    ELSE FALSE
                    END AS is_simulated
                    RETURN labels, is_simulated, numberOfNodes ORDER BY labels[0]
                '''

        return Query(query_str=query_str)

    @staticmethod
    def get_edge_count_query() -> Query:
        # language=SQL
        query_str = '''
                    // List all rel types and counts
                    MATCH (from) - [r] -> (to)
                    WHERE type(r) <> "EXTRACTED_FROM"
                    // WHERE r.type is  NULL
                    WITH Type(r) as type, count(r) as numberOfRelations, CASE
                    WHEN from.simulated OR to.simulated THEN TRUE
                    ELSE FALSE
                    END AS is_simulated
                    RETURN type, is_simulated, numberOfRelations ORDER BY type
                '''

        return Query(query_str=query_str)

    @staticmethod
    def get_model_ids_query():
        query_str = '''
            MATCH (n:GraphModel:Instance)
            WHERE n.name <> "DomainKnowledge"
            RETURN elementId(n) as model_id
        '''

        return Query(query_str=query_str)
