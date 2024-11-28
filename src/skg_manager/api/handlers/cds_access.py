import json
import os
from typing import List, Dict, Union

import pandas as pd
import requests
from flask import current_app

from skg_manager.api.handlers import get_temp_dir


def read_ksjon() -> Dict[str, Union[str, Dict[str, str]]]:
    """ Read in  the key cloak file

    :return: The keycloak file stored as a dictionary
    """
    # Opening JSON file
    f = open(current_app.config.get("EDM_KEYCLOAK_URL"))

    # returns JSON object as a dictionary
    kjson = json.load(f)

    return kjson


def get_edm_token(kjson: Dict[str, Union[str, Dict[str, str]]]) -> str:
    """ Request the edm token from the keycloak server

    :param kjson: a dictionary containing the key
    :return: the access token
    """
    res = requests.post(
        f'{current_app.config.get("SSO_EDM_TOKEN_URL")}/auth/realms/{kjson["realm"]}/protocol/openid-connect/token',
        data={"grant_type": "client_credentials"},
        auth=(kjson["resource"], kjson["credentials"]["secret"]),
    )
    return res.json()["access_token"]


def get_file_names_of_cds(token: str, namespace: str) -> List[str]:
    """Request the defined file names in the Common Data Space


    :param token: a token that for the authorization to request the file names that are defined in the CDS
    :return: A sorted list of file names defined in the CDS
    @param namespace:
    """
    entities_mapping = requests.get(
        f'{current_app.config.get("EDM_BASE_URL")}/{namespace}/entities/map',
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer " + token,
        }
    )

    # read the entities_mapping and extract the file_names
    entities_mapping = json.loads(entities_mapping.text)
    files = [entity_mapping["name"] for entity_mapping in entities_mapping]
    files.sort()
    return files


def retrieve_file(token: str, file_cds: str, namespace: str) -> pd.DataFrame:
    """
    Retrieve the data from the common data space using the file name as specified in the cds
    :param token: a token that for the authorization to request the file names that are defined in the CDS
    :param file_cds: the file name as stored in the cds
    :return: the data requested by the file stored in a dataframe
    @param namespace:
    """

    print(f"Retrieving file {file_cds}")
    res = requests.get(
        f'{current_app.config.get("EDM_BASE_URL")}/{namespace}/entities/data/{file_cds}',
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer " + token,
        }
    )

    df = pd.DataFrame(json.loads(res.text))
    return df


def select_sample(df_log: pd.DataFrame, start_date: str = "29/01/2024", end_date: str = "25/02/2024") -> pd.DataFrame:
    """Select sample of dataset using the start and end date

    @param df_log: dataframe to be sampled
    @param start_date: start date of the sample
    @param end_date: end date of the sample
    @return:
    """
    df_log['date_time_conv'] = pd.to_datetime(df_log["followUpDate"], format="%d/%m/%Y")
    df_log = df_log.loc[df_log["date_time_conv"].between(start_date, end_date)]
    df_log = df_log.drop(columns=['date_time_conv'])
    return df_log


def create_file_name(file_cds: str) -> str:
    """
    Add the csv extension to the file name
    :param file_cds: the name of the file stored in the cds
    :return: file name extended with .csv
    """
    file_name = f"{file_cds}.csv"

    # this file is renamed in the new namespace of the CDS, so we need to rename it as well when working with the old
    # namespace
    if file_cds == "P1_Dirty_Material_Entry":
        file_name = "P1_Material_Entry.csv"

    return file_name


def get_files_from_cds(namespace, already_imported_logs: List[str], defined_files: List[str]):
    """ Method that determines the files to be retrieved and requests these files

    :param already_imported_logs: List of names ensuring we are not re-retrieving double files
    :param defined_files: List of file names that are defined in the data set description
        If a file is retrieved that is not defined a ValueError is thrown
    :param temp_dir: the directory where the files should be temporarily stored
    @param default_namespace:
    @param route_data:
    :return: None

    :raises :class:`ValueError`: if one of the files in the CDS is not defined to be imported into the SKG"

    """

    temp_dir = get_temp_dir()
    token = get_edm_token(read_ksjon())
    files_in_cds = get_file_names_of_cds(token, namespace=namespace)

    for file_cds in files_in_cds:
        file_name = create_file_name(file_cds)
        if file_name not in defined_files:  # check whether a definition exists for the given file
            error_message = f"The file {file_name} is not defined to be imported into the SKG"
            raise ValueError(error_message)

        if file_name not in already_imported_logs:  # check whether the file is not imported yet
            df = retrieve_file(token=token, file_cds=file_cds, namespace=namespace)
            df.to_csv(os.path.join(temp_dir, file_name))
