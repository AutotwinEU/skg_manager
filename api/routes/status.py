# third-party HTTP client library

from flask import Blueprint, current_app, make_response
from neo4j.exceptions import ServiceUnavailable

status_routes = Blueprint("status", __name__)


@status_routes.route("/")
def test_server():
    return make_response(
        'Server is up and running!',
        200
    )


@status_routes.route("/use_case")
def get_use_case_name():
    return make_response(
        'Croma',
        200
    )


@status_routes.route("/namespaces")
def get_namespaces():
    return make_response(
        ['CROMA', 'CROMA_V2'],
        200
    )

@status_routes.route("/entity_types")
def get_optional_entity_types():
    return make_response(
        ['Clean Kits (only for namespace=CROMA)', 'Kit', 'Pouch'],
        200
    )


@status_routes.route("/connection")
def test_connection():
    try:
        current_app.connection.driver.verify_connectivity()
    except ServiceUnavailable:
        return make_response(
            'No connection to the Neo4j database could be made because the service is unavailable. \n'
            'Check whether the database is up and running!',
            500
        )
    except:
        return make_response(
            'No connection the Neo4j database could be made',
            500
        )
    else:
        return make_response(
            'Successful connection',
            200
        )
