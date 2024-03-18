import json
import re

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp

from ..utils import load_json_from_path_or_variable, save_json, load_json
from ..config import entity_list


class Extraction:
    def __init__(
        self,
        llm_input=None,
        llm_path=None,
        save_output=False,
        path_output=None,
    ):
        self.llm_input = llm_input
        self.llm_path = llm_path
        self.save_output = save_output
        self.path_output = path_output

    def run(self):
        data = load_json_from_path_or_variable(self.llm_input, self.llm_path)

        patients_entities = create_patients_entities(data, entity_list)

        if self.save_output:
            save_json(data=patients_entities, path=self.path_output)

        return patients_entities

    def load(self):
        output = load_json(self.path_output)
        return output


def find_string_matches(text, entity_string):
    matches = re.finditer(re.escape(entity_string), text)
    indices = [(match.start(), match.end()) for match in matches]
    return indices


def load_quantised_universal_ner(n_gpu_layers=1, n_batch=512):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path="../models/quantized_q4_1.gguf",
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        f16_kv=True,
        callback_manager=callback_manager,
        verbose=True,
    )

    return llm


def get_universal_ner_entity(input_text, entity_name, llm):
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


def create_patients_entities(data, entity_list):
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
