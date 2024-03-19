import pandas as pd
from typing import List, Dict, Any, Callable


def preprocess_extracted_output(
    patient_entities: List[Dict[str, Any]],
    entities: List[str],
    cleaning_functions_per_entity: Dict[str, List[Callable]],
) -> pd.DataFrame:
    """
    This function takes a list of patient entities along with a list of entity names and
    a dictionary mapping entity names to lists of cleaning functions. It creates a DataFrame
    from the extracted patient entities, applying the specified cleaning functions to each entity.

    Args:
        patient_entities (List[Dict[str, Any]]): A list of dictionaries with a list of entities extract from each patient.
        entities (List[str]): A list of entity names. These names correspond to keys in the dictionaries
                              contained in `patient_entities`.
        cleaning_functions_per_entity (Dict[str, List[Callable]]): A dictionary mapping entity names to lists of cleaning functions.
                                                                   Each cleaning function takes an entity value as input and returns the cleaned value.

    Returns:
        pd.DataFrame: A DataFrame containing the preprocessed data for each entity name type.
    """

    df = create_df_from_patient_entities(
        patient_entities, entities, cleaning_functions_per_entity
    )

    return df


def create_df_from_patient_entities(
    patient_entities: List[Dict[str, Any]],
    entity_list: List[str],
    cleaning_functions_per_entity: Dict[str, List[Callable]],
) -> pd.DataFrame:
    """
    This function constructs a DataFrame from patient entities based on the specified
    list of entities and cleaning functions per entity.

    Args:
        patient_entities (List[Dict[str, Any]]): A list of dictionaries representing entities extracted out from each patient.
        entity_list (List[str]): A list of entity names to extract from the patient entities.
        cleaning_functions_per_entity (Dict[str, List[Callable]]): A dictionary mapping entity names to lists of cleaning functions.

    Returns:
        pd.DataFrame: The DataFrame is created by extracting the specified entities from the patient entities
                      and applying the corresponding cleaning functions.

    """

    patient_data = dict()

    for entity in entity_list:
        cleaning_functions = cleaning_functions_per_entity[entity]
        entity_list = return_list_of_entities_from_patient_entities(
            patient_entities, entity, cleaning_functions
        )
        patient_data[entity] = entity_list

    return pd.DataFrame(patient_data)


def return_list_of_entities_from_patient_entities(
    patient_entities: List[Dict[str, Any]],
    entity_type: List[str],
    cleaning_functions: List[Callable] = list(),
) -> List[List[str]]:
    """
    Extracts a list of entities of a specified type from each patient entity
    and applies optional cleaning functions to each extracted entity.

    Args:
        patient_entities (List[Dict[str, Any]]): A list of dictionaries representing patient entities.
        entity_type (List[str]): A list of entity types to extract from the patient entities.
        cleaning_functions (List[Callable], optional): A list of cleaning functions to apply to each extracted entity.

    Returns:
        List[List[str]]: A list of lists where each inner list contains the extracted entities of the specified type from each patient entity.
    """
    outputs = []
    for patient_entity in patient_entities:
        item = return_list_of_entities_from_person(
            patient_entity["Entities"], entity_type, cleaning_functions
        )
        if len(item) > 0:
            outputs.append(item)
        else:
            outputs.append([])
    return outputs


def get_entity_values(
    person_entities: List[Dict[str, Any]], entity_type: str
) -> List[Dict[str, Any]]:
    """
    This function filters a list of person entities to extract only the entities of a specified type.

    Args:
        person_entities (List[Dict[str, Any]]): A list of dictionaries representing person entities.
        entity_type (str): The type of entity to extract from the person entities.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the entities of the specified type extracted from the person entities.
    """
    return [dict for dict in person_entities if dict["Type"] == entity_type]


def return_list_of_entities_from_person(
    person_entity: List[Dict[str, Any]],
    entity_type: str,
    cleaning_functions: List[Callable] = list(),
) -> List[str]:
    """
    This function filters a list of person entities to extract only the entities of a specified type,
    applies optional cleaning functions to each extracted entity, and returns a list of cleaned entities.

    Args:
        person_entity (List[Dict[str, Any]]): A list of dictionaries representing person entities.
        entity_type (str): The type of entity to extract from the person entities.
        cleaning_functions (List[Callable], optional): A list of cleaning functions to apply to each
                                                       extracted entity. Defaults to an empty list.

    Returns:
        List[str]: A list of cleaned entity values extracted from the person entities.

    """
    person_entity = get_entity_values(person_entity, entity_type)
    entity_list = []
    for entity in person_entity:
        entity_output = entity["Text"]
        for func in cleaning_functions:
            entity_output = func(entity_output)
        if entity_output != "":
            entity_list.append(entity_output)

    return entity_list
