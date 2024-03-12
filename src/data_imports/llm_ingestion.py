import json


def load_llm_data():
    """Laods in the llm dataset

    Returns:
        list: This is a list of a 1000 string outputs created using a large language model to
              generate medical notes from a 1000 patients from a sunthea dataset.
    """
    with open("./data/llm_dataset.json") as f:
        data = json.load(f)

    return data
