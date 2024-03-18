from src.standardise_extraction.preprocess_functions import clean_name
from src.standardise_extraction.standardise_columns import standardise_dates

### COMPONENT OUTPUT PATHS ###
data_folder = "../data"
path_output_synthea = data_folder + "/synthea.json"
path_output_llm = data_folder + "/llm.json"
path_output_extraction = data_folder + "/generative.json"
path_output_standardisation = data_folder + "/standardisation.json"

### GENERATIVE CONFIG: SYNTHEA PATHS ###
path_synthea = "../../synthea"
path_csv = path_synthea + "/output/csv"
path_patients = path_csv + "/patients.csv"
path_encounters = path_csv + "/encounters.csv"

### GENERATIVE CONFIG: SYNTHEA COLUMNS ###
cols_patients = ["Id", "BIRTHDATE", "FIRST", "LAST"]
cols_encounters = ["PATIENT", "ENCOUNTERCLASS", "REASONDESCRIPTION"]

### GENERATIVE CONFIG: SYNTHEA TO LLM LABREL MAPPING ###
cols = {
    "NHS_NUMBER": "NHS_NUMBER",
    "BIRTHDATE": "DATE_OF_BIRTH",
    "FIRST": "GIVEN_NAME",
    "LAST": "FAMILY_NAME",
    "REASONDESCRIPTION": "DIAGNOSIS",
}

### EXTRACTION CONFIG: ENTITIES EXTRACTED ###
entity_list = ["person", "nhs number", "date of birth", "diagnosis"]

### STANDARDISATION CONFIG: PREPROCESSING AND STANDARDISATION DICTIONARY ###
extra_preprocess_functions_per_entity = {"person": [clean_name.remove_titles]}
standardise_functions_per_entity = {
    "date of birth": standardise_dates.normalise_date_column
}
