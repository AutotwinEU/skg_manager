from promg import Query


class IndexQueryLibrary:
    @staticmethod
    def get_set_record_include_range_query() -> Query:
        # language=SQL
        query_str = '''
                CREATE RANGE INDEX record_include_range 
                IF NOT EXISTS FOR (r:Record) ON (r.include)
        '''
        return Query(query_str=query_str)
