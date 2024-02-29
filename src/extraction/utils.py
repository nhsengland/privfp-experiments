import pickle


def save_patients_entities(patients_entities, filename):
    folderpath = f"./notebooks/extraction_module/data/{filename}.pickle"
    with open(folderpath, "wb") as f:
        pickle.dump(patients_entities, f)


def load_patients_entities(filename):
    folderpath = f"./notebooks/extraction_module/data/{filename}.pickle"
    with open(folderpath, "rb") as f:
        saved_patients_entities = pickle.load(f)
    return saved_patients_entities
