import pickle


def save_patients_entities(patients_entities):
    with open("./notebooks/extraction_module/data/patient_entities.pickle", "wb") as f:
        pickle.dump(patients_entities, f)


def load_patients_entities():
    with open("./notebooks/extraction_module/data/patient_entities.pickle", "rb") as f:
        saved_patients_entities = pickle.load(f)
    return saved_patients_entities
