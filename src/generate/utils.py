from .config import (
    path_synthea,
    path_patients,
    path_encounters,
    cols_patients,
    cols_encounters,
    cols,
)

import os
import subprocess
import nhs_number
import pandas as pd
import json


def run_subprocess(commands):
    cwd = os.getcwd()
    os.chdir(path_synthea)

    subprocess.run(
        commands, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )

    os.chdir(cwd)


def append_nhs_numbers(df_input):
    nhs_numbers = nhs_number.generate(quantity=len(df_input))
    df_output = df_input.copy().assign(NHS_NUMBER=nhs_numbers)

    return df_output


def preprocess_patients(df_input):
    df_output = append_nhs_numbers(df_input)

    return df_output


def preprocess_encounters(df_input):
    df_output = df_input.copy()

    df_output = df_output[
        (df_output["ENCOUNTERCLASS"] != "wellness")
        & (df_output["REASONDESCRIPTION"].notna())
    ].drop_duplicates(subset="PATIENT")

    return df_output


def csvs_to_df():
    df_patients_data = pd.read_csv(path_patients)[cols_patients]
    df_encounters_data = pd.read_csv(path_encounters)[cols_encounters]

    df_patients = preprocess_patients(df_patients_data)
    df_encounters = preprocess_encounters(df_encounters_data)

    df_output = df_patients.join(df_encounters.set_index("PATIENT"), on="Id")[
        cols.keys()
    ].rename(columns=cols)[cols.values()]

    return df_output


def df_to_json(df_input):
    array = []

    for i in range(len(df_input)):
        array.append(df_input.iloc[i].to_dict())

    output = json.dumps(array)

    return output


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(data)


def load_synthea_output(path):
    with open(path) as file:
        data = json.load(file)

    batch = []

    for i in range(len(data)):
        batch.append({"data": json.dumps(data[i])})

    return batch
