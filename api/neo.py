from flask import Flask, current_app

# tag::import[]
from neo4j import GraphDatabase
from promg import DatabaseConnection, Configuration, Performance

# end::import[]

"""
Initiate the configuration file in PromG
"""
# tag::initConfiguration[]
def init_promg_configuration(semantic_header_path, dataset_description_path, import_directory, db_name, uri, user,
                             password, verbose, batch_size, use_sample, use_preprocessed_files):
    config = Configuration(
        semantic_header_path=semantic_header_path,
        dataset_description_path=dataset_description_path,
        import_directory=import_directory,
        db_name=db_name,
        uri=uri,
        user=user,
        password=password,
        verbose=verbose,
        batch_size=batch_size,
        use_sample=use_sample,
        use_preprocessed_files=use_preprocessed_files)

    return config


# end::initConfiguration[]

# tag::getConfiguration[]
def get_promg_configuration(is_simulation=False):
    if is_simulation:
        return current_app.promg_promg_sim_config
    else:
        return current_app.promg_config


# end::getConfiguration[]

# tag::initPerformance[]
def init_performance(performance_path):
    current_app.performance = Performance(performance_path, write_console=True)


# end::initPerformance[]

# tag::getPerformance[]
def get_performance():
    return current_app.performance


# end::getPerformance[]
