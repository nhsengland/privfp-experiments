import json
import ast
import pandas as pd
import numpy as np
from itertools import product
import concurrent.futures

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp

from src.ner_pipeline.llm_ingestion import load_llm_data


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
    patients_entities = {}

    for patient_num in range(len(data)):
        input_text = data[patient_num]
        patient_entities = {}
        for entity in entities:
            output = get_universal_ner_entity(input_text, entity, llm)
            patient_entities[entity] = {
                "output": output,
                "output_type": type(output),
            }

        patients_entities[patient_num] = patient_entities

    return patients_entities


def create_patient_entity_table(patient_entities):
    patient_values = []
    llm_data = load_llm_data()

    for id, patient_entities in patient_entities.items():
        text = llm_data[id].strip()
        for entity_name, outputs in patient_entities.items():
            output_type = isinstance(outputs["output_type"], list)
            if output_type:
                output_length = len(outputs["output"])
            else:
                output_length = np.nan

            output = {
                "patient_id": id,
                "entity_name": entity_name,
                "output": outputs["output"],
                "output_length": output_length,
                "output_type": int(output_type),
                "text": text,
            }

            patient_values.append(output)

    patient_entity_table = pd.DataFrame(patient_values)
    patient_entity_table["output_any"] = (
        patient_entity_table["output_length"] >= 1
    )
    patient_entity_table["output_any"] = patient_entity_table[
        "output_any"
    ].astype(int)

    return patient_entity_table


def load_expected_patient_entities_20():
    with open(
        "./src/ner_pipeline/data/expected_patient_entities.json", "r"
    ) as json_file:
        # Load JSON data
        expected_patient_entities = json.load(json_file)

    expected_patient_df = pd.DataFrame(expected_patient_entities).T
    expected_patient_df = (
        expected_patient_df.reset_index()
        .melt(
            id_vars="index",
            var_name="entity_name",
            value_name="expected_output",
        )
        .rename(columns={"index": "patient_id"})
    )
    expected_patient_df["patient_id"] = expected_patient_df[
        "patient_id"
    ].astype(int)
    expected_patient_df["expected_output_length"] = expected_patient_df[
        "expected_output"
    ].apply(len)
    return expected_patient_df


def combine_patient_entities_with_expected_20(patient_entities):
    patient_entity_table = create_patient_entity_table(patient_entities)
    expected_patient_df = load_expected_patient_entities_20()
    merged_df = pd.merge(
        patient_entity_table,
        expected_patient_df,
        on=["patient_id", "entity_name"],
        how="inner",
    )
    merged_df["output_length_match"] = (
        merged_df["output_length"] == merged_df["expected_output_length"]
    )
    merged_df[merged_df["output_length"] == 0]
    return merged_df
