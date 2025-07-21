from __future__ import annotations

import os

## ======================================================
from flask import Flask
from flask_cors import CORS
from promg import Configuration

## ======================================================
from .swagger import swagger_ui_blueprint
from .exceptions.badrequest import BadRequestException
from .exceptions.validation import ValidationException
## ======================================================
## ======================================================
from .router.internal_routers.db_manager_internal_router import DatabaseManagerInternalRouter
from .router.internal_routers.oced_pg_internal_router import OcedPgInternalRouter
from .router.internal_routers.performance_internal_router import PerformanceInternalRouter
from .router.internal_routers.usecase_internal_router import StatusInternalRouter
from .router.internal_routers.kpi_internal_router import KPIInternalRouter
## ======================================================
## ======================================================
from .router.stub_routers.oced_pg_router_stub import OcedPgRouterStub
from .router.stub_routers.performance_router_stub import PerformanceRouterStub
from .router.stub_routers.use_case_router_stub import UseCaseRouterStub
from .router.stub_routers.db_manager_router_stub import DatabaseManagerRouterStub
from .router.stub_routers.kpi_router_stub import KPIRouterStub

def init_promg_configuration(semantic_header_path,
                             dataset_description_path,
                             db_name, uri, user,
                             password, verbose, batch_size, use_sample, use_preprocessed_files):
    config = Configuration(
        semantic_header_path=semantic_header_path,
        dataset_description_path=dataset_description_path,
        db_name=db_name,
        uri=uri,
        user=user,
        password=password,
        verbose=verbose,
        batch_size=batch_size,
        use_sample=use_sample,
        use_preprocessed_files=use_preprocessed_files)

    return config


def getenv_bool(name: str, default_value: bool | None = None) -> bool:
    true_ = ('true', '1', 't')  # Add more entries if you want, like: `y`, `yes`, `on`, ...
    false_ = ('false', '0', 'f')  # Add more entries if you want, like: `n`, `no`, `off`, ...
    value: str | None = os.getenv(name, None)
    if value is None:
        if default_value is None:
            raise ValueError(f'Variable `{name}` not set!')
        else:
            value = str(default_value)
    if value.lower() not in true_ + false_:
        raise ValueError(f'Invalid value `{value}` for variable `{name}`')
    return value in true_


class SKGApp:
    def __init__(self, test_config=None):
        self._app = Flask(__name__)
        cors = CORS(self._app)
        self._set_up_config()
        self._set_test_config(test_config=test_config)

        self._registered_blueprints = {}

    def get_registered_blueprints(self, name):
        if name not in self._registered_blueprints:
            self._registered_blueprints[name] = False

        return self._registered_blueprints[name]

    def set_registered_blueprints(self, name, value):
        if name not in self._registered_blueprints:
            raise KeyError(f'Key `{name}` is not a known blueprint!')

        self._registered_blueprints[name] = value

    def _register_not_set_routers(self):
        self._register_swagger_router()
        self.register_use_case_router()
        self.register_db_manager_router()
        self.register_oced_pg_router()
        self.register_performance_router()
        self.register_kpi_router()

    def get_app(self):
        self._register_not_set_routers()
        return self._app

    def run(self, host, port, debug=False):
        self._register_not_set_routers()
        self._app.run(host=host, port=port, debug=debug)

    def _set_up_error_handling(self):
        # ensure the instance folder exists
        try:
            os.makedirs(self._app.instance_path)
        except OSError:
            pass

        def handle_bad_request(err):
            return {"message": str(err)}, 400

        self._app.register_error_handler(400, handle_bad_request)

        def handle_validation_exception(err):
            return {"message": str(err)}, 422

        self._app.register_error_handler(422, handle_validation_exception)

        def handle_not_found_exception(err):
            return {"message": str(err)}, 404

        self._app.register_error_handler(404, handle_not_found_exception)

    def _set_test_config(self, test_config=None):
        # Apply Test Config
        if test_config is not None:
            self._app.config.update(test_config)

    def _set_up_config(self):
        self._app.config.from_mapping(
            SSO_EDM_TOKEN_URL=os.getenv('SSO_EDM_TOKEN_URL'),
            EDM_BASE_URL=os.getenv('EDM_BASE_URL'),
            EDM_KEYCLOAK_URL=os.getenv('EDM_KEYCLOAK_URL'),
            NEO4J_URI=os.getenv('NEO4J_URI'),
            NEO4J_USERNAME=os.getenv('NEO4J_USERNAME'),
            NEO4J_DB_NAME=os.getenv('NEO4J_DB_NAME'),
            NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')
        )

    def get_database_credentials(self):
        return {
            "uri": self._app.config.get("NEO4J_URI"),
            "user": self._app.config.get("NEO4J_USERNAME"),
            "db_name": self._app.config.get("NEO4J_DB_NAME"),
            "password": self._app.config.get('NEO4J_PASSWORD')
        }

    def register_db_manager_router(self, db_manager_router=None):
        router_name = 'db_manager_router'
        blueprint_is_registered = self.get_registered_blueprints(name=router_name)
        if not blueprint_is_registered:
            db_manager_router = db_manager_router if db_manager_router is not None else DatabaseManagerRouterStub()
            db_manager_internal_router = DatabaseManagerInternalRouter(implementation=db_manager_router)
            self._app.register_blueprint(db_manager_internal_router.db_manager_routes)

            self.set_registered_blueprints(name=router_name, value=True)

    def register_oced_pg_router(self, oced_pg_router=None):
        router_name = 'oced_pg_router'

        blueprint_is_registered = self.get_registered_blueprints(name=router_name)
        if not blueprint_is_registered:
            oced_pg_router = oced_pg_router if oced_pg_router is not None else OcedPgRouterStub()
            oced_pg_internal_router = OcedPgInternalRouter(implementation=oced_pg_router)
            self._app.register_blueprint(oced_pg_internal_router.oced_pg_routes)

            self.set_registered_blueprints(name=router_name, value=True)

    def register_use_case_router(self, use_case_router=None):
        router_name = 'use_case_router'
        blueprint_is_registered = self.get_registered_blueprints(name=router_name)

        if not blueprint_is_registered:
            use_case_router = use_case_router if use_case_router is not None else UseCaseRouterStub()
            status_internal_router = StatusInternalRouter(use_case_implementation=use_case_router)
            self._app.register_blueprint(status_internal_router.use_case_routes)

            self.set_registered_blueprints(name=router_name, value=True)

    def _register_swagger_router(self):
        router_name = 'swagger_router'
        blueprint_is_registered = self.get_registered_blueprints(name=router_name)

        if not blueprint_is_registered:
            self._app.register_blueprint(swagger_ui_blueprint)
            self.set_registered_blueprints(name=router_name, value=True)

    def register_performance_router(self, performance_router=None):
        router_name = 'performance_router'
        blueprint_is_registered = self.get_registered_blueprints(name=router_name)

        if not blueprint_is_registered:
            performance_router = performance_router if performance_router is not None else PerformanceRouterStub()
            performance_internal_router = PerformanceInternalRouter(implementation=performance_router)
            self._app.register_blueprint(performance_internal_router.performance_routes)
            self.set_registered_blueprints(name=router_name, value=True)

    def register_kpi_router(self, kpi_router=None):
        router_name = 'kpi_router'
        blueprint_is_registered = self.get_registered_blueprints(name=router_name)

        if not blueprint_is_registered:
            kpi_router = kpi_router if kpi_router is not None else KPIRouterStub()
            kpi_internal_router = KPIInternalRouter(implementation=kpi_router)
            self._app.register_blueprint(kpi_internal_router.kpi_routes)
            self.set_registered_blueprints(name=router_name, value=True)
