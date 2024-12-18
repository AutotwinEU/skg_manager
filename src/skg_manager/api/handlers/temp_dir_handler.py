import os
import shutil


def get_temp_dir(working_dir="") -> os.path:
    """
    Get and create the temporary directory to store the groundtruth data
    @return: an os.Path indicating where the data is stored
    """

    temp_dir = os.path.join(working_dir, "data", "groundtruth", "raw")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def delete_temp_dir(working_dir: str = ""):
    """
    Delete the temporary directory and its contents

    @return: None
    """

    temp_dir = get_temp_dir(working_dir=working_dir)
    shutil.rmtree(temp_dir)
