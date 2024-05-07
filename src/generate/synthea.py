from src.config import (
    path_synthea,
    path_patients,
    path_encounters,
    cols_patients,
    cols_encounters,
    cols,
)

import nhs_number
import pandas as pd
import os
import subprocess
from typing import Any, Dict, List, Tuple

from src.utils import save_json, load_json


def append_nhs_numbers(df_input: pd.DataFrame) -> pd.DataFrame:
    """
    Appends NHS numbers to a DataFrame.

    Args:
        df_input (DataFrame): Input DataFrame to which NHS numbers will be appended.

    Returns:
        DataFrame: DataFrame with NHS numbers appended as a new column 'NHS_NUMBER'.
    """
    nhs_numbers = nhs_number.generate(quantity=len(df_input))
    df_output = df_input.copy().assign(NHS_NUMBER=nhs_numbers)

    return df_output


def preprocess_patients(df_input: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses patient data by appending NHS numbers.

    Args:
        df_input (DataFrame): Input DataFrame containing patient data.

    Returns:
        DataFrame: DataFrame with NHS numbers appended as a new column 'NHS_NUMBER'.
    """
    df_output = append_nhs_numbers(df_input)

    return df_output


def preprocess_encounters(df_input: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses encounter data by filtering out wellness encounters and removing duplicates based on patient.

    Args:
        df_input (DataFrame): Input DataFrame containing encounter data.

    Returns:
        DataFrame: DataFrame with wellness encounters filtered out and duplicates removed based on patient.
    """
    df_output = df_input.copy()

    df_output = df_output[
        (df_output["ENCOUNTERCLASS"] != "wellness")
        & (df_output["REASONDESCRIPTION"].notna())
    ].drop_duplicates(subset="PATIENT")

    return df_output


def csvs_to_df() -> pd.DataFrame:
    """Reads patient and encounter data from CSV files, preprocesses them, and joins them based on patient ID.

    Returns:
        pd.DataFrame: DataFrame containing preprocessed and joined patient and encounter data.
    """
    df_patients_data = pd.read_csv(path_patients)[cols_patients]
    df_encounters_data = pd.read_csv(path_encounters)[cols_encounters]

    df_patients = preprocess_patients(df_patients_data)
    df_encounters = preprocess_encounters(df_encounters_data)

    df_output = df_patients.join(df_encounters.set_index("PATIENT"), on="Id")[
        cols.keys()
    ].rename(columns=cols)[cols.values()]

    return df_output


def df_to_json(df_input: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Converts a DataFrame to a list of dictionaries (JSON-like format).

    Args:
        df_input (DataFrame): Input DataFrame to be converted.

    Returns:
        List[Dict[str, Any]]: List of dictionaries representing DataFrame rows.
    """
    array = []

    for i in range(len(df_input)):
        array.append(df_input.iloc[i].to_dict())

    return array


class GenerateSynthea:
    """
    Class for generating Synthea data and managing output.

    Methods:
        run: Run Synthea generation with specified commands.
        load: Load previously generated Synthea output from file.
    """

    def __init__(
        self, save_output: bool = False, path_output: str = None
    ) -> None:
        """
        Initializes GenerateSynthea object.

        Args:
            save_output (bool): Whether to save the output to a file.
            path_output (str): Path to the output file.
        """
        self.save_output = save_output
        self.path_output = path_output

    def run(self, *commands: List[str]) -> List[Dict[str, Any]]:
        """
        Run Synthea generation with specified commands.

        Args:
            *commands (List[str]): List of commands to run Synthea.

        Returns:
            List[Dict[str, Any]]: Synthea output as a list of dictionaries.
        """

        output = create_synthea_output(commands)

        if self.save_output:
            save_json(output, self.path_output)

        return output

    def load(self) -> List[Dict[str, Any]]:
        """
        Load previously generated Synthea output from file.

        Returns:
            List[Dict[str, Any]]: Loaded Synthea output as a list of dictionaries.
        """
        output = load_json(self.path_output)
        return output


def create_synthea_output(commands: List[str]) -> List[Dict[str, Any]]:
    """
    Creates Synthea output by running specified commands.

    Args:
        commands (List[str]): List of commands to run Synthea.

    Returns:
        List[Dict[str, Any]]: Synthea output as a list of dictionaries.
    """
    cwd = os.getcwd()
    os.chdir(path_synthea)

    subprocess.run(
        commands, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )

    os.chdir(cwd)

    df = csvs_to_df()
    output = df_to_json(df)
    return output
