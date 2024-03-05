path_synthea = "../../synthea"
path_csv = path_synthea + "/output/csv"
path_patients = path_csv + "/patients.csv"
path_encounters = path_csv + "/encounters.csv"
path_synthea_output = "../data/synthea.json"

cols_patients = ["Id", "BIRTHDATE", "FIRST", "LAST"]
cols_encounters = ["PATIENT", "ENCOUNTERCLASS", "REASONDESCRIPTION"]
cols = {
    "NHS_NUMBER": "NHS_NUMBER",
    "BIRTHDATE": "DATE_OF_BIRTH",
    "FIRST": "GIVEN_NAME",
    "LAST": "FAMILY_NAME",
    "REASONDESCRIPTION": "DIAGNOSIS",
}

path_llm_output = "../data/llm.json"
