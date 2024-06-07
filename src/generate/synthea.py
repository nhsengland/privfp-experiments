import nhs_number
import pandas as pd
import os
import subprocess
from typing import Any, Dict, List, Tuple

from src.utils import save_json, load_json, file_exists
from src.config.global_config import GlobalConfig
from src.config.experimental_config import SyntheaConfig


cols_patients = ["Id", "BIRTHDATE", "FIRST", "LAST"]
cols_encounters = ["PATIENT", "ENCOUNTERCLASS", "REASONDESCRIPTION"]
cols = {
    "NHS_NUMBER": "NHS_NUMBER",
    "BIRTHDATE": "DATE_OF_BIRTH",
    "FIRST": "GIVEN_NAME",
    "LAST": "FAMILY_NAME",
    "REASONDESCRIPTION": "DIAGNOSIS",
}


class GenerateSynthea:
    """
    Class for generating Synthea data and managing output.

    Methods:
        run: Run Synthea generation with specified commands or load if the data alreadys exists.
    """

    def __init__(
        self, global_config: GlobalConfig, syntheaconfig: SyntheaConfig
    ) -> None:
        """
        Initializes GenerateSynthea object.

        Args:
            global_config (GlobalConfig): This is a pydantic typing model that contains configuration parameters from global config.
            SyntheaConfig (SyntheaConfig): This is a pydantic typed class which has values for
                                           population_num, county, and path_output
        """
        SyntheaConfig.model_validate(syntheaconfig.model_dump())

        self.population_num = syntheaconfig.population_num
        self.county = syntheaconfig.county
        self.path_output = syntheaconfig.path_output
        self.global_config = global_config

    def run_or_load(
        self,
        extra_commands: List[str] = list(),
        resave: bool = False,
        save: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Run Synthea generation with specific commands, or loads a model from path given.

        Args:
            commands (List[str]): List of commands to run Synthea.
            resave (bool): Whether to resave the output. Defaults to False.
            Determines whether you want to save any files, if this is false it doesn't save any files. Defaults to True.

        Returns:
            List[Dict[str, Any]]: Synthea output as a list of dictionaries.
        """

        if file_exists(self.path_output) and resave is False:
            output = load_json(self.path_output)
        else:
            # Defines the fixed commands handle by configuration, and allows a user to add additional commands.
            commands = [
                "./run_synthea",
                "-p",
                self.population_num,
                self.county,
            ] + extra_commands
            output = create_synthea_output(
                global_config=self.global_config, commands=commands
            )

            if save:
                if resave or file_exists(self.path_output) is False:
                    save_json(output, self.path_output)

        return output


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


def csvs_to_df(global_config: GlobalConfig) -> pd.DataFrame:
    """Reads patient and encounter data from CSV files, preprocesses them, and joins them based on patient ID.

    Args:
        global_config (GlobalConfig): This is a pydantic typing model that contains configuration parameters from global config.

    Returns:
        pd.DataFrame: DataFrame containing preprocessed and joined patient and encounter data.
    """
    path_patients = (
        global_config.synthea.path_synthea + "/output/csv/patients.csv"
    )
    path_encounters = (
        global_config.synthea.path_synthea + "/output/csv/encounters.csv"
    )
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


def create_synthea_output(
    global_config: GlobalConfig, commands: List[str]
) -> List[Dict[str, Any]]:
    """
    Creates Synthea output by running specified commands.

    Args:
        global_config (GlobalConfig): This is a pydantic typing model that contains configuration parameters from global config.
        commands (List[str]): List of commands to run Synthea.

    Returns:
        List[Dict[str, Any]]: Synthea output as a list of dictionaries.
    """
    cwd = os.getcwd()
    os.chdir(global_config.synthea.path_synthea)

    try:
        subprocess.run(
            commands, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
    except e as e:
        raise (e)
    finally:
        os.chdir(cwd)

    df = csvs_to_df(global_config=global_config)
    output = df_to_json(df)
    return output
