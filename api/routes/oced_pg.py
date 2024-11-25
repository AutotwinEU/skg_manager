import os
import shutil
from flask import Blueprint, make_response

from ..exceptions.exception_handler import db_exception_handler
from ..util.util import get_methods, get_namespace, get_entity_types_list, get_timespan
from ..util.cds_manager import request_ground_truth_files_from_cds

oced_pg_routes = Blueprint("ocedpg", __name__, url_prefix="/oced_pg")


def get_temp_dir() -> os.path:
    """
    Get and create the temporary directory to store the groundtruth data
    @return: an os.Path indicating where the data is stored
    """

    temp_dir = os.path.join("data", "groundtruth", "raw")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def delete_temp_dir():
    """
    Delete the temporary directory and its contents

    @return: None
    """

    methods = get_methods()
    if not methods.is_simulated_data:
        temp_dir = get_temp_dir()
        shutil.rmtree(temp_dir)


def request_and_store_files_from_cds():
    """
    Request and store the ground truth data from CDS
    @return: None
    """

    methods = get_methods()
    temp_dir = get_temp_dir()
    namespace = get_namespace()

    if not methods.is_simulated_data:
        already_imported_logs = methods.get_imported_logs()
        defined_files = methods.get_defined_file_names()
        request_ground_truth_files_from_cds(already_imported_logs, defined_files, temp_dir, namespace)


def load_records_into_skg():
    """
    Load records into SKG database and trim them
    @return:
    """

    methods = get_methods()
    methods.preprocess_files()
    methods.load_data()


@oced_pg_routes.route('/load', methods=['POST'])
@db_exception_handler
def load_records_route():
    """
    Load the records from the Common Data Space into the SKG.

    @return: None
    """

    request_and_store_files_from_cds()
    load_records_into_skg()
    delete_temp_dir()

    return make_response(
        'Loaded data into database!',
        200
    )


def filter_records(methods):
    if not methods.is_simulated_data:  # filter when dealing with ground truth data
        entity_types = get_entity_types_list()
        start_date, end_date = get_timespan()
        methods.filter_record_layer(entity_types=entity_types,
                                    start_date=start_date,
                                    end_date=end_date)


@oced_pg_routes.route('/transform', methods=['POST'])
@db_exception_handler
def transform_records():
    """
    Transform the records stored in the SKG into the semantic layer

    @return:
    """
    methods = get_methods()
    filter_records(methods)
    methods.transform_data()

    return make_response(
        'Transformed data using semantic header!',
        200
    )


@oced_pg_routes.route('/delete_simulated_data', methods=['POST'])
@db_exception_handler
def delete_simulated_data():
    """
    Delete the simulation data

    @return:
    """
    methods = get_methods(is_simulation_data=True)
    methods.delete_data()

    return make_response(
        'Deleted simulated data!',
        200
    )
