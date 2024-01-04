import json

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from langchain import LLMChain
from langchain.prompts import PromptTemplate


def upload_quantised_universal_ner(n_gpu_layers=1, n_batch=512):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path="../../models/quantized_q4_1.gguf",
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        f16_kv=True,
        callback_manager=callback_manager,
        verbose=True,
    )

    return llm


def get_universal_ner_entity(input_text, entity_name, llm):
    # This strip the text of any special text characters \n etc.
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
    patients_entities = {}

    for patient_num in range(len(data)):
        input_text = data[patient_num]
        patient_entities = {}
        for entity in entities:
            output = get_universal_ner_entity(input_text, entity, llm)
            patient_entities[entity] = {"output": output, "output_type": type(output)}

        patients_entities[patient_num] = patient_entities

    return patients_entities
