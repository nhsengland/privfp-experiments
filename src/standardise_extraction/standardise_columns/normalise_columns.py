from dateparser import parse
import pandas as pd


def normalise_date_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Takes in the name of a column inside the dataframe and
    transforms all dates in that column using date parser.

    Args:
        df (pd.DataFrame): A dataframe with a date column we want to transform.
        column_name (str): The name of the date column to transform.

    Returns:
        pd.DataFrame: Returns a dataframe with the date column transformed.
    """
    df_copy = df.copy()
    df_copy[column_name] = df_copy[column_name].astype(str).apply(parse)
    return df_copy
