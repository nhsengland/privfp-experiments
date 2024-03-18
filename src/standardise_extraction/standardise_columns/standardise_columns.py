import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Dict


def standardise_preprocess_output(df, standardise_functions_per_entity=dict()):

    for column_name, func in standardise_functions_per_entity.items():
        df = func(df, column_name)

    encoded_output, lookup = encode(df)

    return [encoded_output, lookup]


def encode(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]:
    """Encode a dataset for processing by pycorrectmatch

    :param df: Table of data
    :returns: Table of encoded data and lookup dictionary"""
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
