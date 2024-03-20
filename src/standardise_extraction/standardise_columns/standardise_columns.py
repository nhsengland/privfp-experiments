import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Dict, List, Callable


def standardise_preprocess_output(
    df: pd.DataFrame,
    standardise_functions_per_entity: Dict[str, List[Callable]] = dict(),
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

    for column_name, functions in standardise_functions_per_entity.items():
        for func in functions:
            df = func(df, column_name)

    encoded_output, lookup = encode(df)

    return [encoded_output, lookup]


def extract_first_entity_from_list(df: pd.DataFrame, column_name: str):
    """
    For the given column_name it extracts the first entity from the list of row value inputs.

    Args:
        df (pd.DataFrame): Dataframe created from the preprocessing functon module.
        column_name (str): The name of the column whose inputs are a list.

    Returns:
        (pd.DataFrame) : Dataframe where the inputs of the columns have had their first input extracted.
    """
    df[column_name] = df[column_name].apply(extract_first_entity)
    return df


def extract_first_entity(input: List[str]):
    """
    Extracts the first entity from the input list.

    Args:
        input (List[str]): A list of strings containing entities.

    Returns:
        Optional[str]: The first entity from the input list, or None if the list is empty.
            If the list is not empty, the returned value is a string representing the first entity.
            If the list is empty, the function returns None.
    """
    if len(input) > 0:
        return input[0]
    else:
        return None


def encode(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]:
    """
    Encode a dataset for processing by pycorrectmatch

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
    """
    Extends the sklearn LabelEncoder class for use in scikit-learn pipelines.

    This class provides methods to fit and transform labels, suitable for use within
    scikit-learn pipelines.

    Methods:
        fit_transform(self, y, _) -> Transform labels into normalized integers and reshape the result.
        transform(self, y, _) -> Transform labels into normalized integers and reshape the result.

    Example Usage:
        # Create an instance of PipelineLabelEncoder
        encoder = PipelineLabelEncoder()

        # Fit and transform labels
        encoded_labels = encoder.fit_transform(["a", "b", "c"])

        # Transform new labels using fitted encoder
        new_encoded_labels = encoder.transform(["b", "c", "d"])
    """

    def fit_transform(self, y, _, *args, **kwargs):
        """
        Fit the encoder to the labels and transform them into normalized integers.

        Args:
            y : array-like of shape (n_samples,)
                The target variable to encode.
            _ : Ignored
                Placeholder parameter to match the sklearn interface.
            *args : Additional positional arguments
                Additional arguments to pass to the parent class method.
            **kwargs : Additional keyword arguments
                Additional keyword arguments to pass to the parent class method.

        Returns:
            transformed_y : ndarray of shape (n_samples, 1)
                The transformed labels, reshaped to a column vector.
        """
        return super().fit_transform(y, *args, **kwargs).reshape(-1, 1)

    def transform(self, y, _, *args, **kwargs):
        """
        Transform labels into normalized integers and reshape the result.

        Args:
            y : array-like of shape (n_samples,)
                The target variable to encode.
            _ : Ignored
                Placeholder parameter to match the sklearn interface.
            *args : Additional positional arguments
                Additional arguments to pass to the parent class method.
            **kwargs : Additional keyword arguments
                Additional keyword arguments to pass to the parent class method.

        Returns:
            transformed_y : ndarray of shape (n_samples, 1)
                The transformed labels, reshaped to a column vector.
        """
        return super().transform(y, *args, **kwargs).reshape(-1, 1)
