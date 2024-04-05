import os
import julia
import pandas as pd
import numpy as np
from julia.api import Julia
from typing import Dict, List


class PrivacyRiskScorer:
    """A scorer using PyCorrectMatch that takes a pd.DataFrame and calculates
    population uniqueness, fits a Gaussian copula and calculates individual uniqueness scores.
    """

    def __init__(self):
        path_julia = os.popen("which julia").read().strip()
        julia.install(julia=path_julia)
        Julia(compiled_modules=False, runtime=path_julia)
        import correctmatch  # noqa E402

        correctmatch.precompile()

        self.correctmatch = correctmatch
        self.fitted_model = None
        self.size = 0

    def calculate_population_uniqueness(self, df: pd.DataFrame) -> float:
        return self.correctmatch.uniqueness(df.values)

    def fit(self, df):
        """
        Fit a Gaussian copula model to a discrete multivariate dataset
        The fitted model is a Julia object with the estimated model.
        The argument `exact_marginal`=True ensures that the marginal distributions
        are categorical, whose values range from 1 to number_of_unique_values for each feature.
        """
        self.size = df.shape[0]
        self.look_up = self.create_lookup_dict(df)
        self.fitted_model = self.correctmatch.fit_model(
            df.values, exact_marginal=True
        )

    def create_lookup_dict(
        self, df: pd.DataFrame
    ) -> Dict[str, Dict[int, int]]:
        """
        Create a dictionary with one key per column and another dictionary
        as a value. That inner dictionary has the mapping between the value of the
        record and the marginal distribution value it corresponds to for a fitted copula.

        :param df: pd.DataFrame to be scored
        :returns Dictionary that maps real feature values to the values of the marginal
        distributions of the copula model.
        """
        record_to_copula = {
            col: dict(
                zip(
                    df[col].value_counts().index,
                    range(1, df[col].nunique() + 1),
                )
            )
            for col in df.columns.to_list()
        }
        return record_to_copula

    def map_record_to_copula(self, row: pd.Series) -> List[int]:
        """Convert real dataset values of a record to values that correspond to
        the marginal distributions of the fitted copula using the look up dictionary.

        :param row: pd.Series to be transformed from real values to the values of the
        marginal distributions of the copula model
        :returns List of integer values, the transformed record
        """
        if self.fitted_model is None:
            raise Exception("Please fit the model first.")
        return [self.look_up[col][row.loc[col]] for col in row.index]

    def get_individual_uniqueness(self, row: pd.Series) -> float:
        """Estimate individual uniquess for one given record.

        :param row: pd.Series to be transformed from real values to the values of the
        marginal distributions of the copula model
        :returns the individual uniqueness score of the single record
        """
        if self.fitted_model is None:
            raise Exception("Please fit the model first.")
        return self.correctmatch.individual_uniqueness(
            self.fitted_model, self.map_record_to_copula(row), self.size
        )

    def predict(self, df: pd.DataFrame) -> pd.Series:
        """Return the individual privacy risk scores of the original records

        :param df: pd.DataFrame of the real records to be scored
        :returns pd.Series of the individual uniqueness scores for all records in the df.
        """
        transformed_df = self.map_records_to_copula(df)
        return pd.Series(
            self.predict_transformed(transformed_df),
            index=df.index,
            name="individual_uniqueness_score",
        )

    def map_records_to_copula(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert real dataset values of a dataframe to values that correspond
        to the marginal distributions of the fitted copula using the look up dictionary.

        :param df: pd.DataFrame of the real records to be scored
        :returns pd.DataFrame of the transformed records, their values correpond to their
        representations of the marginal distributions of the copula model.
        """
        if self.fitted_model is None:
            raise Exception("Please fit the model first.")
        transformed_df = pd.concat(
            [
                df[col].replace(self.look_up[col]).to_frame()
                for col in df.columns
            ],
            axis=1,
        )
        return transformed_df

    def score_func(self, transformed_row: List[int]) -> float:
        """Estimate individual uniquess for a tranformed record.

        :param transformed_row: List of integer values that correpond to the
        representation of the record given the marginal distributions of the copula model.
        :returns the individual uniqueness score of the single transformed
        record
        """
        if self.fitted_model is None:
            raise Exception("Please fit the model first.")
        return self.correctmatch.individual_uniqueness(
            self.fitted_model,
            transformed_row,
            self.size,
        )

    def predict_transformed(self, transformed_df: pd.DataFrame) -> np.ndarray:
        """Return the privacy risk scores of the transformed records

        :param transformed_df: pd. DataFrame of the transformed records to be scored
        :returns np.ndarray of the individual uniqueness scores for all transformed records
        in the transformed_df
        """
        return np.apply_along_axis(
            self.score_func, 1, transformed_df.astype("int")
        )

    def re_identify(
        self, individual_uniqueness: float, pop_size: int = 0
    ) -> float:
        """Calculate the likelihood of re-identifcation given the individual uniqueness

        :param individual_uniqueness: output of the get_individual_uniqueness
        :param pop_size: the size of the population
        :returns float result of the re-identifcation formula as described in the PCM paper
        """
        if pop_size == 0:
            if self.size == 0:
                raise Exception("Please fit model first")
            pop_size = self.size
        elif pop_size == 1:
            raise ValueError("Population size has to be higher than 1.")

        re_id = (1 / pop_size) * (
            (1 - individual_uniqueness ** (pop_size / (pop_size - 1)))
            / (1 - individual_uniqueness ** (1 / (pop_size - 1)))  # noqa: W503
        )
        return re_id
