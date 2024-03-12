from dateparser import parse


def normalise_date_column(df, column_name):
    df_copy = df.copy()
    df_copy[column_name] = df_copy[column_name].astype(str).apply(parse)
    return df_copy
