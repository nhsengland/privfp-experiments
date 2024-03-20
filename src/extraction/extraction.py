import json
import re

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from typing import List, Dict, Any, Optional, Tuple

from src.utils import load_json_from_path_or_variable, save_json, load_json
from src.config import entity_list, universal_ner_path


class Extraction:
    """
    Class that extracts entities from a list of llm generated medical notes.
    """

    def __init__(
        self,
        llm_input: Optional[List[str]] = None,
        llm_path: Optional[str] = None,
        save_output: Optional[bool] = False,
        path_output: Optional[str] = None,
    ):
        """Self-defined arguments

        Args:
            llm_input (Optional[List[str]], optional): This is a list of llm generated medical notes. Defaults to None.
            llm_path (Optional[str], optional): This is the path to a JSON list of llm generated medical notes. Defaults to None.
            save_output (Optional[bool], optional): This determines whether the extraction JSON is saved to path_output. Defaults to False.
            path_output (Optional[str], optional): This provides the path of where the JSON extraction output should sit. Defaults to None.
        """
        self.llm_input = llm_input
        self.llm_path = llm_path
        self.save_output = save_output
        self.path_output = path_output

    def run(self) -> List[Dict[str, Any]]:
        """This returns a list of dictionaries that has an 'Entities' property of a
        list of entity dictionaries for each person.

        Returns:
            List[Dict[str, Any]]: List of dictionaries that has an 'Entities' property of a
                                  list of entity dictionaries for each person.
        """

        data = load_json_from_path_or_variable(self.llm_input, self.llm_path)

        patients_entities = create_patients_entities(data, entity_list)

        if self.save_output:
            save_json(data=patients_entities, path=self.path_output)

        return patients_entities

    def load(self) -> List[Dict[str, Any]]:
        """Loads the patient entities from a given path.

        Returns:
            List[Dict[str, Any]]: List of dictionaries that has an 'Entities' property of a
                                  list of entity dictionaries for each person.
        """
        patient_entities = load_json(self.path_output)
        return patient_entities


def find_string_matches(text: str, entity_string: str) -> List[Tuple]:
    """Takes in a text string and returns a list of tuples of the start and end indexes for every
    time the entity_string occurs in the text.

    Args:
        text (str): Total string that entities have been extracted from.
        entity_string (str): The entity value that has been extracted.

    Returns:
        List[Tuple]: List of tuples with the start and end indexes of when the entity
                     has occured in the given text.
    """
    matches = re.finditer(re.escape(entity_string), text)
    indices = [(match.start(), match.end()) for match in matches]
    return indices


def load_quantised_universal_ner(
    n_gpu_layers: int = 1, n_batch: int = 512
) -> LlamaCpp:
    """

    Args:
        n_gpu_layers (int, optional): This is the number of gpu's used to run the model.
                                      Defaults to 1, as the majority of machines have 1.
        n_batch (int, optional): This determines how the prompt tokens is batched up and
                                 processed by the model.

    Returns:
        LlamaCpp: Returns a llamacpp object to run universal NER locally.
    """
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path=universal_ner_path,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        f16_kv=True,
        callback_manager=callback_manager,
        verbose=True,
    )

    return llm


def get_universal_ner_entity(
    input_text: str, entity_name: str, llm: LlamaCpp
) -> List[Any]:
    """
    Uses the LLamaCpp object to extract entities, for a given entity name, from the input text provided.

    Args:
        input_text (str): This is a llm generated medical record.
        entity_name (str): This is the name of the entity given to universal NER to help extrct.
        llm (LlamaCpp): This reutrns a configured LlamaCpp pipeline to run universal NER.

    Returns:
        List[Any]: Returns a list of entities that have been extracted with the given entity_name.
    """

    prompt_template = """
    USER: Text: {input_text}
    ASSISTANT: I’ve read this text.
    USER: What describes {entity_name} in the text?
    ASSISTANT: (model's predictions in JSON format)
    """
    input_text = input_text.strip()

    prompt = prompt_template.format_map(
        {"input_text": input_text, "entity_name": entity_name}
    )

    output = llm(prompt)
    output = json.loads(output)

    return output


def create_patients_entities(
    data: List[str], entity_list: List[str]
) -> List[Dict[str, Any]]:
    """This creates the patient entities JSON from the list of llm generated medical notes.

    Args:
        data (List[str]): This is a list of llm generated medical notes.
        entity_list (List[str]): This is a list of entity names given to the model.

    Returns:
        List[Dict[str, Any]]: This returns a list of a dictionary with an Entities property
                              which is a list of each entity.
    """
    llm = load_quantised_universal_ner()
    patients_entities = []

    for patient_num in range(len(data)):
        input_text = data[patient_num]
        patient_entities = []
        for entity in entity_list:
            outputs = get_universal_ner_entity(input_text, entity, llm)
            for output in outputs:
                match_indices = find_string_matches(input_text, output)
                each_output = {
                    "Text": output,
                    "Type": entity,
                    "Match_Count": len(match_indices),
                    "Match_Indices": match_indices,
                }
                patient_entities.append(each_output)

        patients_entities.append({"Entities": patient_entities})

    return patients_entities
