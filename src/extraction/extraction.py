import json
import re

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp


def run(data, entities):
    llm = upload_quantised_universal_ner()
    patients_entities = []

    for patient_num in range(len(data)):
        input_text = data[patient_num]
        patient_entities = []
        for entity in entities:
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


def find_string_matches(text, entity_string):
    matches = re.finditer(re.escape(entity_string), text)
    indices = [(match.start(), match.end()) for match in matches]
    return indices


def upload_quantised_universal_ner(n_gpu_layers=1, n_batch=512):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path="./models/quantized_q4_1.gguf",
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


def generate_patients_entities(data, entities):
    llm = upload_quantised_universal_ner()
    patients_entities = []

    for patient_num in range(len(data)):
        input_text = data[patient_num]
        patient_entities = []
        for entity in entities:
            outputs = get_universal_ner_entity(input_text, entity, llm)
            for output in outputs:
                each_output = {"Text": output, "Type": entity}
                patient_entities.append(each_output)

        patients_entities.append({"Entities": patient_entities})

    return patients_entities
