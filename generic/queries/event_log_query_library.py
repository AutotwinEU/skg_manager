from promg import Query


class EventLogExtractorQueryLibrary:

    @staticmethod
    def get_create_event_log_query(df_type,
                                   entity_type,
                                   event_attributes=None,
                                   corr_type="ACTS_ON",
                                   entity_attributes=None) -> Query:
        if event_attributes is None:
            event_attributes = ["activity", "timestamp"]
        if entity_attributes is None:
            entity_attributes = ["sysId"]
        event_attributes_str = ", ".join([f"e.{attribute} as {attribute}" for attribute in event_attributes])
        entity_attributes_str = ", ".join([f"n.{attribute} as {attribute}" for attribute in entity_attributes])

        # language=sql
        query_str = '''
                    MATCH path = (start_event:Event) - [:$df_type*] -> (end_event)
                    MATCH (start_event) - [:ACTS_ON] -> (n) - [:IS_OF_TYPE] -> ({entityType:$entity_type})
                    WHERE NOT EXISTS ((:Event) - [:$df_type] -> (start_event))
                    AND NOT EXISTS ((end_event) - [:$df_type] -> (:Event))
                    UNWIND nodes(path) as e
                    RETURN 
                        right(elementId(e), 5) as eventId,
                        $event_attributes_str,
                        $entity_attributes_str   
                    '''

        return Query(query_str=query_str,
                     template_string_parameters={
                         "df_type": df_type,
                         "event_attributes_str": event_attributes_str,
                         "entity_attributes_str": entity_attributes_str,
                         "corr_type": corr_type
                     },
                     parameters={
                         "entity_type": entity_type
                     }
                     )
