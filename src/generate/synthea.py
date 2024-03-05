from .config import path_synthea_output
from .utils import run_subprocess, csvs_to_df, df_to_json, save


def run(*commands):
    run_subprocess(commands)
    df = csvs_to_df()
    data = df_to_json(df)
    save(path_synthea_output, data)
