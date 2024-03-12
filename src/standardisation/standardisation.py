from src.standardisation.preprocess_extracted_output import (
    preprocess_extracted_output,
)
from src.standardisation.standardise_preprocess_output import (
    standardise_preprocess_output,
)


def run(
    patient_entities,
    entity_list,
    extra_preprocess_functions_per_entity=dict(),
    standardise_functions_per_entity=dict(),
):

    empty_functions = [[] for i in entity_list]
    preprocess_functions_per_entity = dict(zip(entity_list, empty_functions))

    preprocess_functions_per_entity.update(
        extra_preprocess_functions_per_entity
    )

    preprocess_functions_per_entity.update(
        extra_preprocess_functions_per_entity
    )

    df = preprocess_extracted_output(
        patient_entities,
        entity_list,
        preprocess_functions_per_entity,
    )

    standardised_df, lookup = standardise_preprocess_output(
        df, standardise_functions_per_entity
    )

    return standardised_df
