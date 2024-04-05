import pandas as pd
from typing import List, Dict, Any, Optional

from src.standardise_extraction.preprocess_functions.preprocess_functions import (
    preprocess_extracted_output,
)
from src.standardise_extraction.standardise_columns.standardise_columns import (
    standardise_preprocess_output,
)

from src.utils import (
    load_json_from_path_or_variable,
    save_dataframe_to_csv,
    load_dataframe_from_csv,
)
from src.config import (
    extra_preprocess_functions_per_entity,
    standardise_functions_per_entity,
    entity_list,
)


class StandardiseExtraction:
    """This standardises the outputs from the extraction part ready for pycorrect match."""

    def __init__(
        self,
        extraction_input: Optional[List[Dict[str, Any]]] = None,
        extraction_path: Optional[str] = None,
        save_output: Optional[bool] = False,
        path_output: Optional[str] = None,
    ):
        """Self-defined arguments

        Args:
            extraction_input (Optional[List[Dict[str, Any]]], optional): This is a list of dictionaries with an entities property with a
                                                                         list of dictionary for each entity extracted. Defaults to None.
            extraction_path (Optional[str], optional): This is the path to a list of dictionaries. Defaults to None.
            save_output (Optional[bool], optional): This determines whether the extraction JSON is saved to path_output. Defaults to False.
            path_output (Optional[str], optional): This provides the path of where the JSON extraction output should sit. Defaults to None.
        """
        self.extraction_input = extraction_input
        self.extraction_path = extraction_path
        self.save_output = save_output
        self.path_output = path_output

    def run(self) -> pd.DataFrame:
        """Returns a dataframe of the first entitiy extracted from each entity type given
           for each medical note given.

        Returns:
            pd.DataFrame: Dataframe of the first entity extracted for a given entity type.
        """

        # TODO: FIX THIS - THIS WON'T WORK? MAYBE TRY AND SAVE AS A NUMPY ARRAY AND CONVERT BACK?
        patient_entities = load_json_from_path_or_variable(
            self.extraction_input, self.extraction_path
        )

        empty_functions = [[] for i in entity_list]
        preprocess_functions_per_entity = dict(
            zip(entity_list, empty_functions)
        )

        preprocess_functions_per_entity.update(
            extra_preprocess_functions_per_entity
        )

        # This preprocesses entities extracted from the extraction process.
        df = preprocess_extracted_output(
            patient_entities,
            entity_list,
            preprocess_functions_per_entity,
        )

        # This standardises columns that have been extracted out from the dataframe.
        standardised_df, _ = standardise_preprocess_output(
            df, standardise_functions_per_entity
        )

        if self.save_output:
            save_dataframe_to_csv(standardised_df, self.path_output)

        # This converts the values into a numpy array
        return standardised_df

    def load(self) -> pd.DataFrame:
        """Loads the standardised dataframe from file.

        Returns:
            pd.DataFrame: Dataframe of the first entity extracted for a given entity type.
        """
        standardised_df = load_dataframe_from_csv(self.path_output)
        return standardised_df
