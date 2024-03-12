from .utils import run_subprocess, csvs_to_df, df_to_json


def run(*commands):
    run_subprocess(commands)
    df = csvs_to_df()
    output = df_to_json(df)

    return output
