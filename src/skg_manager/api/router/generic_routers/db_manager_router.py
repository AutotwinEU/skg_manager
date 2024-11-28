from colorama import Fore
from neo4j.exceptions import ServiceUnavailable

from src.skg_manager.api.router.interface_routers.db_manager_router_interface import DatabaseManagerRouterInterface
from src.skg_manager.api.router.router_result import Result
from src.skg_manager.generic.service_interfaces.db_manager_interface import DatabaseManagerInterface


class DatabaseManagerRouter(DatabaseManagerRouterInterface):

    def __init__(self, db_manager: DatabaseManagerInterface):
        self.db_manager = db_manager

    def on_clear_db(self) -> Result:
        try:
            self.clear_db()
            return Result(status=Result.Status.SUCCESS, message='Database Cleared!')
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def clear_db(self):
        print(Fore.RED + 'Clearing the database.' + Fore.RESET)
        self.db_manager.clear_db(replace=False)
        self.set_constraints()

    def set_constraints(self):
        if not self.constraints_have_been_set():
            self.db_manager.set_constraints(entity_key_name="internalId")

    def constraints_have_been_set(self):
        constraints = self.db_manager.get_constraints()
        return len(constraints) > 0

    def on_get_statistics(self) -> Result:
        try:
            item_list = self.get_statistics()
            return Result(status=Result.Status.SUCCESS, message="Successfully requested statistics", data=item_list)
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def get_statistics(self):
        result = self.db_manager.get_statistics()

        item_list = {"records": [], "nodes": [], "relationships": [], "nodeCount": 0, "edgeCount": 0}

        for item in result:
            if "labels" in item:
                label = ":".join(item["labels"])
                count = item["numberOfNodes"]
                is_simulated = item["is_simulated"]
                item_list["nodes"].append({"label": label, "count": count, "is_simulated": is_simulated})
                item_list["nodeCount"] += count
            elif "log" in item:
                log = item["log"]
                count = item["numberOfNodes"]
                is_simulated = item["is_simulated"]
                item_list["records"].append({"log": log, "count": count, "is_simulated": is_simulated})
            elif "type" in item:
                _type = item["type"]
                count = item["numberOfRelations"]
                is_simulated = item["is_simulated"]
                item_list["relationships"].append({"type": _type, "count": count, "is_simulated": is_simulated})
                item_list["edgeCount"] += count

        return item_list

    def on_get_timespan(self) -> Result:
        try:
            item_list = self.db_manager.get_timespan()
            return Result(status=Result.Status.SUCCESS, message="Successfully requested timespan", data=item_list)
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_get_records_timespan(self) -> Result:
        try:
            item_list = self.db_manager.get_records_time_span()
            return Result(status=Result.Status.SUCCESS, message="Successfully requested record timespan",
                          data=item_list)
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_get_logs(self) -> Result:
        try:
            logs = self.db_manager.get_imported_logs()
            log_result = {"logs": logs}
            return Result(status=Result.Status.SUCCESS, message="Successfully requested logs",
                          data=log_result)
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def on_get_event_log(self, entity_type) -> Result:
        try:
            event_log = self.get_event_log(entity_type)
            if event_log is None:
                event_log = []
            return Result(status=Result.Status.SUCCESS, message="Successfully requested event log",
                          data=event_log)
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def get_event_log(self, entity_type):
        return self.db_manager.get_event_log(entity_type)

    def on_get_model_ids(self) -> Result:
        # TODO add timestamps constraints
        try:
            model_ids = self.get_model_ids()
            if model_ids is None:
                model_ids = []

            return Result(status=Result.Status.SUCCESS, message="Successfully requested model ids",
                          data=model_ids)
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))

    def get_model_ids(self):
        return self.db_manager.get_model_ids()

    def on_test_connection(self) -> Result:
        try:
            self.db_manager.test_connection()
            return Result(status=Result.Status.SUCCESS, message='Connection established')
        except ServiceUnavailable:
            return Result(status=Result.Status.FAILURE,
                          message='No connection to the Neo4j database could be made because the service is '
                                  'unavailable. \n'
                                  'Check whether the database is up and running!')
        except Exception as e:
            return Result(status=Result.Status.FAILURE, message=str(e))
