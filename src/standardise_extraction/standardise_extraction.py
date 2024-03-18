from src.standardise_extraction.preprocess_functions.preprocess_functions import (
    preprocess_extracted_output,
)
from src.standardise_extraction.standardise_columns.standardise_columns import (
    standardise_preprocess_output,
)

from src.utils import (
    load_json_from_path_or_variable,
    save_json,
    load_json,
    save_dataframe_to_csv,
    load_dataframe_from_csv,
)
from src.config import (
    extra_preprocess_functions_per_entity,
    standardise_functions_per_entity,
    entity_list,
)


class StandardiseExtraction:
    def __init__(
        self,
        extraction_input=None,
        extraction_path=None,
        save_output=False,
        path_output=None,
    ):
        self.extraction_input = extraction_input
        self.extraction_path = extraction_path
        self.save_output = save_output
        self.path_output = path_output

    def run(self):

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

        # This standardises given columns that have been extracted out from the dataframe.
        standardised_df, lookup = standardise_preprocess_output(
            df, standardise_functions_per_entity
        )

        if self.save_output:
            save_dataframe_to_csv(standardised_df, self.path_output)

        return standardised_df

    def load(self):
        standardised_df = load_dataframe_from_csv(self.path_output)
        return standardised_df
