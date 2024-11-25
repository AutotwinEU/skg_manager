# third-party HTTP client library
import json

from flask import Blueprint, jsonify, make_response

from ..exceptions.exception_handler import db_exception_handler
from ..util.util import get_methods
db_manager_routes = Blueprint("db_manager", __name__, url_prefix="/db_manager")


@db_manager_routes.route("/test_response")
def test_response():
    return make_response(
        'Test worked!',
        200
    )


@db_manager_routes.route('/clear_db', methods=['GET', 'POST'])
@db_exception_handler
def clear_db_route():
    methods = get_methods()
    methods.clear_db()

    return make_response(
        'Database Cleared!',
        200
    )


@db_manager_routes.route('/statistics', methods=['GET'])
@db_exception_handler
def get_statistics_route():
    methods = get_methods()
    item_list = methods.get_statistics()
    return jsonify(item_list)


@db_manager_routes.route('/time_span', methods=['GET'])
@db_exception_handler
def get_timespan_route():
    methods = get_methods()
    item_list = methods.get_timespan()
    return jsonify(item_list)


@db_manager_routes.route('/records_time_span', methods=['GET'])
@db_exception_handler
def get_records_timespan_route():
    methods = get_methods()
    item_list = methods.get_records_timespan()
    return jsonify(item_list)


@db_manager_routes.route('/logs', methods=['GET'])
@db_exception_handler
def get_logs_route():
    methods = get_methods()
    result = methods.get_imported_logs()

    return jsonify({"logs": result})


@db_manager_routes.route('/eventlog/<entity_type>', methods=['GET'])
@db_exception_handler
def get_event_logs_route(entity_type):
    # TODO add timestamps contraints
    methods = get_methods()
    event_log = methods.get_event_log(entity_type)
    if event_log is None:
        event_log = []
    result = json.dumps(event_log, default=str)

    return jsonify(result)


@db_manager_routes.route('/get_model_ids', methods=['GET'])
@db_exception_handler
def get_model_ids():
    # TODO add timestamps constraints
    methods = get_methods()
    model_ids = methods.get_model_ids()
    if model_ids is None:
        model_ids = []

    return jsonify(model_ids)
