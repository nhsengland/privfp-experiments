import pandas as pd


def preprocess_extracted_output(
    patient_entities, entities, cleaning_functions_per_entity
):

    df = create_df_from_patient_entities(
        patient_entities, entities, cleaning_functions_per_entity
    )

    return df


def create_df_from_patient_entities(
    patient_entities, entity_list, cleaning_functions_per_entity
):

    patient_data = dict()

    for entity in entity_list:
        cleaning_functions = cleaning_functions_per_entity[entity]
        entity_list = return_list_of_first_entity_from_patient_entities(
            patient_entities, entity, cleaning_functions
        )
        patient_data[entity] = entity_list

    return pd.DataFrame(patient_data)


def return_list_of_first_entity_from_patient_entities(
    patient_entities, entity_type, cleaning_functions=list()
):
    outputs = []
    for patient_entity in patient_entities:
        item = return_list_of_entities_from_person(
            patient_entity["Entities"], entity_type, cleaning_functions
        )
        if len(item) > 0:
            outputs.append(item[0])
        else:
            outputs.append(None)
    return outputs


def get_entity_values(person_entities, entity_type):
    return [dict for dict in person_entities if dict["Type"] == entity_type]


def return_list_of_entities_from_person(
    person_entity, entity_type, cleaning_functions=[]
):
    person_entity = get_entity_values(person_entity, entity_type)
    entity_list = []
    for entity in person_entity:
        entity_output = entity["Text"]
        for func in cleaning_functions:
            entity_output = func(entity_output)
        if entity_output != "":
            entity_list.append(entity_output)

    return entity_list
