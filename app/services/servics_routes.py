from app.queries.mongo_queries import execute_mongo_query
from app.queries.neo4j_queries import execute_neo4j_query


def run_query(query_id: int, filters: dict = None):
    if query_id in range(1, 6):
        return execute_mongo_query(query_id, filters)
    elif query_id in range(6, 11):
        return execute_neo4j_query(query_id, filters)
    else:
        raise ValueError("Invalid query ID")


def get_attack_types_severity(top_5: bool = False):
    query_id = 1
    return run_query(query_id, {"top_5": top_5})


def get_average_casualties_by_region(top_5: bool = False):
    query_id = 2
    return run_query(query_id, {"top_5": top_5})


def get_top_5_terror_groups():
    query_id = 3
    return run_query(query_id)


def get_region_activity_map():
    query_id = 4
    return run_query(query_id)


def get_yearly_change_map():
    query_id = 5
    return run_query(query_id)


def get_expanding_groups():
    query_id = 6
    return run_query(query_id)

def get_frequent_attackers_by_target():
    query_id = 7
    return run_query(query_id)