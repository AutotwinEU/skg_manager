import logging

from promg import DatabaseConnection

from ..queries.performance_queries import PerformanceQueryLibrary as pfql
from ...performance_library.ecdf_library import AnnotatedEcdf, EcdfCollection, deserialize_objects


def create_ecdf_object(exec_time):
    gt_sim = "sim" if exec_time['is_simulated_data'] else "gt"
    input_sensor = exec_time["input_sensor"]
    output_sensor = exec_time["output_sensor"]
    times = exec_time["times"]

    # Create ECDF object
    logging.debug("Creating ECDF object")
    ecdf = AnnotatedEcdf(values=times,
                         input_sensor=input_sensor,
                         output_sensor=output_sensor,
                         gt_sim=gt_sim)
    logging.debug(f"ECDF object created: {ecdf}")
    return ecdf


class PerformanceService:
    def __init__(self, db_connection: DatabaseConnection, working_dir):
        self.connection = db_connection
        self.ecdf_collections = None
        self.working_dir = working_dir

    def remove_performance_artifacts(self):
        self.connection.exec_query(pfql.delete_all_performance_nodes)

    # ==============================================================================
    def add_ecdf_to_collection(self, ecdf, compute_conformance_metrics=True):
        input_sensor = ecdf.input_sensor
        output_sensor = ecdf.output_sensor

        if (input_sensor, output_sensor) in self.ecdf_collections:
            ecdf_collection = self.ecdf_collections[(input_sensor, output_sensor)]
            ecdf_collection.add_ecdf(ecdf, compute_conformance_metrics)
        else:
            ecdf_collection = EcdfCollection(ecdf, title=f"{input_sensor}-{output_sensor}")
            self.ecdf_collections[(input_sensor, output_sensor)] = ecdf_collection

    def create_ecdf_collections(self):
        logging.debug("Starting ecdfc_latency_between_sensors")
        self.ecdf_collections = {}

        try:
            exec_times = self.connection.exec_query(pfql.execution_times_between_sensors)

            logging.debug(f"Execution times fetched: {exec_times}")
            if not exec_times or len(exec_times) == 0:
                logging.warning("No execution times found")
                return None  # Early return if no data is found

            for exec_time in exec_times:
                ecdf = create_ecdf_object(exec_time)
                self.add_ecdf_to_collection(ecdf)

        except Exception as e:
            logging.error(f"Error in ecdfc_latency_between_sensors: {str(e)}",
                          exc_info=True)

    def add_ecdf_collection_to_skg(self):
        print("start add_performance_to_skg")
        for sensors, ecdf_collection in self.ecdf_collections.items():
            self.connection.exec_query(pfql.store_ecfds_in_db,
                                       **{
                                           "name": ecdf_collection.return_title(),
                                           "ecdfs": ecdf_collection.get_ecdfs_to_store(),
                                           "sensors": sensors
                                       })
            for pairs, conformance_metric in ecdf_collection.get_conformance_metrics().items():
                self.connection.exec_query(pfql.add_conformance_between_ecdfs,
                                           **{
                                               "name1": pairs[0],
                                               "name2": pairs[1],
                                               "conformance": conformance_metric
                                           })
        print("finish add_performance_to_skg")

    def create_aggregated_performance_html(self):
        if self.ecdf_collections is None:
            self.retrieve_ecdf_collections_from_skg()
        self.create_index_file()

    def create_index_file(self):
        f = open(self.working_dir + "/index.html", "w")
        f.write("<h2>Ecdfcs</h2>\n")
        for index, ecdf_collection in enumerate(self.ecdf_collections.values()):
            ecdf_collection.plot_to_file(self.working_dir, show=False)
            f.write("<h4>" + ecdf_collection.return_title() + "\n")
            f.write(
                f"<a id='eCDF {index}'></h4><img src='{ecdf_collection.return_title()}.svg'><a href='#top'>back to "
                f"top<a><br>\n")

            f.write("<br>Aggregate values:<br>")
            ecdf_data = ecdf_collection.get_table_of_ecdf_aggregate()
            f.write(ecdf_data.to_html(index=False, justify="left"))

            conformance_data = ecdf_collection.get_conformance_table()
            if len(conformance_data) > 0:
                f.write("<br>Conformance values:<br>")
                f.write(conformance_data.to_html(index=False, justify="left"))
        f.close()

    def retrieve_ecdf_collections_from_skg(self):
        ecdf_collections_from_skg = self.connection.exec_query(pfql.retrieve_all_ecdfs)
        if ecdf_collections_from_skg is None or len(ecdf_collections_from_skg) == 0:
            self.create_ecdf_collections()
        else:
            self.ecdf_collections = {}
            for ecdf_skg_collection in ecdf_collections_from_skg:
                ecdf_list = ecdf_skg_collection['ecdfs']
                deserialized_ecdf_list = [deserialize_objects(ecdf['value']) for ecdf in ecdf_list]
                deserialized_ecdf_list.sort()
                for ecdf in deserialized_ecdf_list:
                    self.add_ecdf_to_collection(ecdf, compute_conformance_metrics=True)
