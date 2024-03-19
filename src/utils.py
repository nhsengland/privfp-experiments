import os
import json
import pandas as pd
from typing import Union, List, Dict, Any


def save_json(
    data: Union[List[str], Dict[str, int], List[Dict[str, int]]], path: str
) -> None:
    """Saves a json serialiable object to a given path.

    Args:
        data (Union[List[str], Dict[str, int], List[Dict[str, int]]]): Either a list or dictionary to save to path.
        path (str): String to define the path location.

    Raises:
        ValueError: If path is undefined.
        ValueError: If no output is availible to save.
    """
    if path is None:
        raise ValueError("The path variable has not been set")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    if data is not None:
        with open(path, "w") as f:
            json.dump(data, f)
    else:
        raise ValueError("No output available to save.")


def load_json(
    path: str,
) -> Union[List[str], Dict[str, int], List[Dict[str, int]]]:
    """Load a JSON seriliable Object that is a list or dictionary.

    Args:
        path (str): String to define the path location.

    Raises:
        ValueError: If path is undefined.

    Returns:
        (Union[List[str], Dict[str, int], List[Dict[str, int]]]): The loaded JSON serilisable object.
    """
    if path is not None:
        with open(path) as file:
            output = json.load(file)
    else:
        raise ValueError("The path variable has not been set")
    return output


def check_variable_path_state(
    from_variable: Union[List[str], Dict[str, int], List[Dict[str, int]]],
    from_path: str,
) -> None:
    """Verifies that either from_variable or from_path has been set.

    Args:
        from_variable (Union[List[str], Dict[str, int], List[Dict[str, int]]]): Given list or dictionary.
        from_path (str): String of a path to a json seralisable object.

    Raises:
        ValueError: If both from_variable and from_path is set.
        ValueError: If neither from_variable and from_path is set.
    """
    if from_variable is None and from_path is None:
        raise ValueError("Either from_variable or from_path must be provided.")
    if from_variable is not None and from_path is not None:
        raise ValueError(
            "Both from_variable and from_path cannot be provided at the same time."
        )


def load_json_from_path_or_variable(
    from_variable: Union[List[Any], Dict[str, Any]], from_path: str
) -> Union[List[str], Dict[str, int], List[Dict[str, int]]]:
    """This determines whether from_variable is used or is read in from path.

    Args:
        from_variable (Union[List[str], Dict[str, int], List[Dict[str, int]]]): JSON seralisable object.
        from_path (str): Path to a JSON seralisable object.

    Returns:
        Union[List[str], Dict[str, int], List[Dict[str, int]]]: A JSON seralise object that is a dictionary or list.
    """

    check_variable_path_state(from_variable, from_path)

    if from_variable is not None:
        json_value = from_variable
    else:
        json_value = load_json(from_path)

    return json_value


def save_dataframe_to_csv(dataframe: pd.DataFrame, path: str) -> None:
    """
    Save a pandas DataFrame to a CSV file.

    Args:
        dataframe (pd.DataFrame): The pandas DataFrame to be saved.
        path (str): The filename for the CSV file.
    """
    dataframe.to_csv(path, index=False)


def load_dataframe_from_csv(path: str) -> pd.DataFrame:
    """
    Load a pandas DataFrame from a CSV file.

    Args:
        path (str): The filename of the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    dataframe = pd.read_csv(path)
    return dataframe
