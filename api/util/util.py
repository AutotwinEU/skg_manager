import json
from typing import Optional

from croma_module.method_manager import Methods
from flask import current_app, request
import os


def get_methods(is_simulation_data: Optional[bool] = None) -> Methods:
    if is_simulation_data is None:
        is_simulation_data = get_is_simulation_data()

    config = current_app.promg_sim_config if is_simulation_data else current_app.promg_config
    methods = current_app.method_creator.factory_method(config=config,
                                                       is_simulation_data=is_simulation_data)
    return methods


def get_is_simulation_data():
    requested_data = request.args.get('is_simulation_data')
    if requested_data is not None:
        is_simulation_data = requested_data.lower() in ['true', '1']
    else:
        is_simulation_data = False
    return is_simulation_data


def get_namespace():
    requested_data = request.args.get('namespace')
    return requested_data if requested_data is not None else "CROMA"


def get_entity_types_list():
    requested_data = request.args.get('entity_types')
    default = ["Clean Kits"]
    if requested_data is None:
        requested_data = default
    else:
        requested_data = json.loads(requested_data.replace("'", '"'))

    # clean kits always take priority over the others
    # i.e. if clean kits is selected, we won't include anything else (e.g. no pouches)
    if "Clean Kits (only for namespace=CROMA)" in requested_data:
        requested_data = default

    return requested_data


def get_timespan():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    start_date = start_date if start_date is not None else "1970-01-01"
    end_date = end_date if end_date is not None else "2970-01-01"

    return start_date, end_date
