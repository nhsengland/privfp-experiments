import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Dict, Any, List


def standardise_preprocess_output(
    df: pd.DataFrame, standardise_functions_per_entity: Dict[str, Any] = dict()
) -> Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]:
    """This takes in a dataframe, and for each given column name provided in the standardise_functions_per_entity dictionary,
        it applies the function given to each colun.

    Args:
        df (pd.DataFrame): This is a dataframe we want to transform given columns on.
        standardise_functions_per_entity (Dict[str, Any], optional): This is a dictionary of column names to a function
                                                                     that can be applied across columns. Defaults to dict().

    Returns:
        Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]: Returns a dataframe that has had columns transformed and has been encoded,
                                                        with an encoded lookup dictionary to help transform results back.
    """

    for column_name, func in standardise_functions_per_entity.items():
        df = func(df, column_name)

    encoded_output, lookup = encode(df)

    return [encoded_output, lookup]


def encode(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]:
    """Encode a dataset for processing by pycorrectmatch

    Args:
        df (pd.DataFrame): This is a dataframe we want to encode column values.

    Returns:
        Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]: Table of encoded data and lookup dictionary.
    """

    output = df.fillna(0)
    for col in output.columns:
        if len(set([type(i) for i in output[col].tolist()])) > 1:
            output[col] = output[col].astype("str")
    ct = ColumnTransformer(
        [
            (f"encode_{col_name}", PipelineLabelEncoder(), col_name)
            for col_name in output.columns
        ]
    )
    encoded_output = pd.DataFrame(
        ct.fit_transform(output), index=output.index, columns=output.columns
    )
    transformers = {k: j for i, j, k in ct.transformers_}
    lookup = {
        i: {k: j for j, k in enumerate(transformers[i].classes_)}
        for i in output.columns
    }
    return encoded_output, lookup


class PipelineLabelEncoder(LabelEncoder):
    def fit_transform(self, y, _, *args, **kwargs):
        return super().fit_transform(y, *args, **kwargs).reshape(-1, 1)

    def transform(self, y, _, *args, **kwargs):
        return super().transform(y, *args, **kwargs).reshape(-1, 1)
