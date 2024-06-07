import json
import re
import os

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp, Ollama
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any, Optional, Tuple, Callable, Union
from gliner import GLiNER

from src.config.experimental_config import ExtractionConfig
from src.config.prompt_template_handler import (
    load_and_validate_extraction_prompt_template,
)
from src.utils import (
    load_json_from_path_or_variable,
    save_json,
    load_json,
    download_llm_model_from_hf,
    file_exists,
)
from src.config.global_config import GlobalConfig


class Extraction:
    """
    Class that extracts entities from a list of llm generated medical notes.
    """

    def __init__(
        self,
        global_config: GlobalConfig,
        extractionconfig: ExtractionConfig,
        llm_input: Optional[List[str]] = None,
    ):
        """Initialising the Extraction Model Class.

        Args:
            global_config (GlobalConfig): This is a pydantic typing model that contains configuration parameters from global config.
            extractionconfig (ExtractionConfig): This is a pydantic typing configuration that contains values on:
                - server_model_type: The type of way you want to serve the model e.g. ollama, local, or gliner.
                - local features: Contains two features from huggingface (hf_repo_id and hf_filename.)
                - ollama_features: Contain one feature which is the ollama_ner_model.
                - prompt_template_path: Path to where the template lives.
                - entity_list: List of entities you want to extract from the model.
                - llm_path: Path to where the LLM has been saved.
                - path_output: Path where we want to save the data output from this component.
            llm_input (Optional[List[str]], optional): This is a list of llm generated medical notes. Defaults to None.
        """
        ExtractionConfig.model_validate(extractionconfig.model_dump())

        self.llm_input = llm_input
        self.llm_path = extractionconfig.llm_path
        self.path_output = extractionconfig.path_output
        self.server_model_type = extractionconfig.server_model_type
        self.entity_list = extractionconfig.entity_list
        self.gliner_model = extractionconfig.gliner_features.gliner_model

        self.hf_repo_id = extractionconfig.local_features.hf_repo_id
        self.hf_filename = extractionconfig.local_features.hf_filename

        self.ollama_ner_model = (
            extractionconfig.ollama_features.ollama_ner_model
        )

        if self.server_model_type == "ollama":
            template_path = f"{global_config.output_paths.extraction_template}/{extractionconfig.ollama_features.prompt_template_path}"
            self.prompt_template = (
                load_and_validate_extraction_prompt_template(template_path)
            )
        elif self.server_model_type == "local":
            template_path = f"{global_config.output_paths.extraction_template}/{extractionconfig.local_features.prompt_template_path}"
            self.prompt_template = (
                load_and_validate_extraction_prompt_template(template_path)
            )
        else:
            self.prompt_template = None

    def run_or_load(
        self,
        verbose: bool = False,
        save: bool = False,
    ) -> List[Dict[str, Any]]:
        """This returns a list of dictionaries that has an 'Entities' property of a
        list of entity dictionaries for each person.

        Args:
            verbose (bool): Determines whether a model ran using langchain is verbose to the user. Defaults to False.
            save (bool): Determines whether you want to save the data on another run. Defaults to False.

        Returns:
            List[Dict[str, Any]]: List of dictionaries that has an 'Entities' property of a
                                  list of entity dictionaries for each person.
        """

        if file_exists(self.path_output) and save is False:
            patients_entities = load_json(self.path_output)
        else:
            data = load_json_from_path_or_variable(
                self.llm_input, self.llm_path
            )

            patients_entities = create_patients_entities(
                data,
                self.entity_list,
                self.server_model_type,
                self.prompt_template,
                gliner_model=self.gliner_model,
                local_hf_filename=self.hf_filename,
                local_hf_repo_id=self.hf_repo_id,
                ollama_ner_model=self.ollama_ner_model,
                verbose=verbose,
            )

            if save is False:
                pass
            else:
                save_json(data=patients_entities, path=self.path_output)

        return patients_entities


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


def load_local_ner_model(
    local_ner_path: str, verbose: bool = True
) -> LlamaCpp:
    """
    Args:
        local_ner_path (str): Path to the location of where a local model has been installed to.
        verbose (bool): Set to True if you want verbose on.
    Returns:
        LlamaCpp: Returns a llamacpp object to run a generative NER model locally.
    """
    callback_manager = CallbackManager([])

    if verbose:
        callback_manager.add_handler(StreamingStdOutCallbackHandler())

    llm = LlamaCpp(
        model_path=local_ner_path,
        n_gpu_layers=1,
        n_batch=512,
        f16_kv=True,
        callback_manager=callback_manager,
        verbose=True,
    )

    return llm


def load_ollama_ner_model(
    ollama_ner_model: str, verbose: bool = True
) -> Ollama:
    """
    Args:
        ollama_ner_model: The name of an ollama model that can be pulled from ollama.

    Returns:
        Ollama: Returns a llamacpp object to run universal NER locally.
    """
    callback_manager = CallbackManager([])

    if verbose:
        callback_manager.add_handler(StreamingStdOutCallbackHandler())

    llm = Ollama(model=ollama_ner_model, callback_manager=callback_manager)

    return llm


def get_entity_from_generative_ner_model(
    input_text: str,
    entity_name: str,
    llm: Union[LlamaCpp, Ollama],
    prompt_template: PromptTemplate = None,
) -> List[Any]:
    """
    Uses the LLamaCpp OR Ollama to extract entities, for a given entity name, from the input text provided.

    Args:
        input_text (str): This is a llm generated medical record.
        entity_name (str): This is the name of the entity given to universal NER to help extrct.
        llm (Union[LlamaCpp, Ollama]): This returns a configured LlamaCpp or Ollama pipeline to run a generative NER model.

    Returns:
        List[Any]: Returns a list of entities that have been extracted with the given entity_name.
    """
    input_text = input_text.strip()

    prompt = prompt_template.format_map(
        {"input_text": input_text, "entity_name": entity_name}
    )

    output = llm(prompt)
    output = json.loads(output)

    return output


def create_entity_output(
    output: List[str], entity: str, match_indices: List[Tuple[int]]
) -> List[Dict[str, Any]]:
    """Takes the outputs from universalNER and reformats to fit the Gliner structure.

    Args:
        output (List[str]): List of strings that have been extracted from the text for a given entity name.
        entity (str): Name of the entity you want to extract out from the text.
        match_indices (List[Tuple[int]]): List of indexes of where the given entity text exists in the given document.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with key values for each entity extracted.
    """

    entity_output = []
    for start, end in match_indices:
        entity_output.append(
            {
                "start": start,
                "end": end,
                "text": output,
                "label": entity,
                "score": 1,
            }
        )
    return entity_output


def create_patient_entities_from_generative_llm(
    model: Union[LlamaCpp, Ollama],
    input_text: str,
    entity_list: List[str],
    prompt_template: str,
) -> List[Dict[str, Any]]:
    """Function used to create entities from a generative LLM that produces a list of entity outputs.

    Args:
        model (Callable): A generative LLM model from localised downloaded model OR Ollama.
        input_text (str): The document fed into the model.
        entity_list (List[str]): The list of entities you want to get out of the model.
        prompt_template (PromptTemplate): This is a prompt that is fed to the ollama or LlamaCPP pipeline.

    Returns:
        List[Dict[str, Any]]: Returns a list of entity dictionaries extracted out of the model.
    """
    patient_entities = []
    for entity in entity_list:
        outputs = get_entity_from_generative_ner_model(
            input_text, entity, model, prompt_template
        )
        for output in outputs:
            match_indices = find_string_matches(input_text, output)
            each_output = create_entity_output(output, entity, match_indices)
            patient_entities += each_output
    return patient_entities


def load_ner_model(
    server_model_type: str,
    gliner_model: str = None,
    local_hf_repo_id: str = None,
    local_hf_filename: str = None,
    ollama_ner_model: str = None,
    verbose: bool = True,
) -> Union[LlamaCpp, Ollama, GLiNER]:
    """A function to load a specific type of NER model.

    Args:
        server_model_type (str): This is the type of way a model is served. Options being "gliner", "local", and "ollama".
        gliner_model (str): This is the name of the gliner model you want to pull in.
        local_hf_repo_id (str, optional): The location of a repo on hugging face that has a .gguf model we want to download. Defaults to None.
        local_hf_filename (str, optional): The name of the filename inside the local_hf_repo_id. Defaults to None.
        ollama_ner_model (str, optional): The ollama model pulled from ollama. Defaults to None.
        verbose (bool): define verbose on whether you want to print outputs to the user. Defaults to True.

    Raises:
        ValueError: Raises an error if "gliner", "local", or "ollama" is not given as the model type,
                    or if corresponding `local_ner_path` or `ollama_ner_model` is None when required.

    Returns:
        Union[LlamaCpp, Ollama, GLiNER]: _description_
    """
    if server_model_type == "gliner":
        if gliner_model is None:
            raise ValueError(
                "For 'gliner' model type, 'gliner_model' must be provided."
            )
        model = GLiNER.from_pretrained(gliner_model)
    elif server_model_type == "local":
        if local_hf_repo_id is None or local_hf_filename is None:
            raise ValueError(
                "For 'local' model type, 'local_hf_repo_id' and 'local_hf_filename' must be provided."
            )
        download_llm_model_from_hf(
            repo_id=local_hf_repo_id, filename=local_hf_filename
        )
        local_ner_path = f"../models/{local_hf_filename}"
        model = load_local_ner_model(local_ner_path, verbose)
    elif server_model_type == "ollama":
        if ollama_ner_model is None:
            raise ValueError(
                "For 'ollama' model type, 'ollama_ner_model' must be provided."
            )
        model = load_ollama_ner_model(ollama_ner_model, verbose)
    else:
        raise ValueError(
            "No valid input provided. Please specify 'server_model_type' as 'gliner', 'local', or 'ollama'"
        )

    return model


def create_patients_entities(
    data: List[str],
    entity_list: List[str],
    server_model_type: str,
    prompt_template: PromptTemplate = None,
    gliner_model: str = None,
    local_hf_repo_id: str = None,
    local_hf_filename: str = None,
    ollama_ner_model: str = None,
    verbose: bool = True,
) -> List[Dict[str, Any]]:
    """This creates the patient entities JSON from the list of llm generated medical notes.

    Args:
        data (List[str]): This is a list of llm generated medical notes.
        entity_list (List[str]): This is a list of entity names given to the model.
        server_model_type (str): This is the type of model used. Options being "gliner", "local", and "ollama".
        prompt_template (PromptTemplate): This is the template used in type of models "local" or "ollama"
        gliner_model (str): The name of the gliner model you want to use to extract entities from.
        local_hf_repo_id (str, optional): The location of a repo on hugging face that has a .gguf model we want to download. Defaults to None.
        local_hf_filename (str, optional): The name of the filename inside the local_hf_repo_id. Defaults to None.
        ollama_ner_model (str, optional): The ollama model pulled from ollama. Defaults to None.
        verbose (bool, optional): This determines whether models run using langchain need verbose on or off.

    Returns:
        List[Dict[str, Any]]: This returns a list of a dictionary with an Entities property
                              which is a list of each entity.
    """
    model = load_ner_model(
        server_model_type,
        gliner_model=gliner_model,
        local_hf_repo_id=local_hf_repo_id,
        local_hf_filename=local_hf_filename,
        ollama_ner_model=ollama_ner_model,
        verbose=verbose,
    )

    total_patients_entities = []

    for patient_num in range(len(data)):
        input_text = data[patient_num]
        if server_model_type == "gliner":
            patient_entities = model.predict_entities(
                input_text, entity_list, threshold=0.5
            )
        else:
            patient_entities = create_patient_entities_from_generative_llm(
                model, input_text, entity_list, prompt_template
            )

        total_patients_entities.append({"Entities": patient_entities})

    return total_patients_entities
