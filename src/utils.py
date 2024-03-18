import os
import json
import pandas as pd
from typing import Any


def save_json(data, path):
    if path is None:
        raise ValueError("The path variable has not been set")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    if data is not None:
        with open(path, "w") as f:
            json.dump(data, f)
    else:
        raise ValueError("No output available to save.")


def load_json(path) -> Any:
    if path is not None:
        with open(path) as file:
            output = json.load(file)
    else:
        raise ValueError("The path variable has not been set")
    return output


def check_variable_path_state(from_variable, from_path):
    if from_variable is None and from_path is None:
        raise ValueError("Either from_variable or from_path must be provided.")
    if from_variable is not None and from_path is not None:
        raise ValueError(
            "Both from_variable and from_path cannot be provided at the same time."
        )


def load_json_from_path_or_variable(from_variable, from_path):

    check_variable_path_state(from_variable, from_path)

    if from_variable is not None:
        json_value = from_variable
    else:
        json_value = load_json(from_path)

    return json_value


def save_dataframe_to_csv(dataframe, path):
    """
    Save a pandas DataFrame to a CSV file.

    Args:
        dataframe (pd.DataFrame): The pandas DataFrame to be saved.
        path (str): The filename for the CSV file.
    """
    dataframe.to_csv(path, index=False)


def load_dataframe_from_csv(path):
    """
    Load a pandas DataFrame from a CSV file.

    Args:
        path (str): The filename of the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    dataframe = pd.read_csv(path)
    return dataframe
