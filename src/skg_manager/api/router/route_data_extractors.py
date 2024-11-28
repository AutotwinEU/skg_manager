import json
from typing import List


def extract_is_simulation_data(route_data) -> bool:
    if "is_simulation_data" in route_data:
        is_simulation_data = route_data["is_simulation_data"].lower() in ['true', '1']
    else:
        is_simulation_data = False
    return is_simulation_data


def extract_entity_types(route_data, default: List[str]) -> List[str]:
    entity_types = []
    if "entity_types" in route_data:
        requested_data = route_data["entity_types"]
        entity_types = json.loads(requested_data.replace("'", '"'))
    if not entity_types:
        entity_types = default

    return entity_types


def extract_timespan(route_data) -> [str, str]:
    start_date = route_data["start_date"] if "start_date" in route_data else "1970-01-01"
    end_date = route_data["end_date"] if "start_date" in route_data else "2970-01-01"

    return start_date, end_date
