from pydantic import BaseModel
import yaml
from typing import Dict, Optional, List


class LocalFeaturesConfig(BaseModel):
    hf_repo_id: Optional[str] = None
    hf_filename: Optional[str] = None
    prompt_template_path: Optional[str] = None


class GlinerFeaturesConfig(BaseModel):
    gliner_model: Optional[str] = None


class OllamaFeaturesConfig(BaseModel):
    ollama_ner_model: Optional[str] = None
    prompt_template_path: Optional[str] = None


class GenerateModelFeaturesConfig(BaseModel):
    llm_model_name: str
    prompt_template_path: str


class ExtractionConfig(BaseModel):
    server_model_type: str
    gliner_features: Optional[GlinerFeaturesConfig]
    local_features: Optional[LocalFeaturesConfig]
    ollama_features: Optional[OllamaFeaturesConfig]
    entity_list: Optional[List] = None
    llm_path: Optional[str] = None
    path_output: Optional[str] = None


class GenerateConfig(BaseModel):
    llm_model_features: GenerateModelFeaturesConfig
    synthea_path: Optional[str] = None
    path_output: Optional[str] = None


class SyntheaConfig(BaseModel):
    population_num: str
    county: str
    path_output: Optional[str] = None


class OutputsConfig(BaseModel):
    experiment_name: str
    save: bool


class Pycorrectmatch(BaseModel):
    privacy_scorer: bool


class Explainers(BaseModel):
    shap: bool


class PyCanon(BaseModel):
    identifiers: List[str]
    quasi_identifiers: List[str]
    sensitive_attributes: List[str]


class ExperimentalConfig(BaseModel):
    outputs: OutputsConfig
    synthea: SyntheaConfig
    generate: GenerateConfig
    extraction: ExtractionConfig
    pycorrectmatch: Pycorrectmatch
    explainers: Explainers
    pycanon: PyCanon


def load_experimental_config(config_path: str) -> ExperimentalConfig:
    """Loads the experimental config with a given configuration path.

    Args:
        config_path (str): Path to where the experimental config lives.

    Returns:
        ExperimentalConfig: Returns a pydantic structured config dictionary.
    """
    with open(config_path, "r") as config_file:
        config_dict = yaml.safe_load(config_file)
        return ExperimentalConfig.model_validate(config_dict)


def reload_as_experimental_config(config_dict: dict) -> ExperimentalConfig:
    """Reloads the experimental config and ensure the config is validated when it's been transformed.

    Args:
        config_dict (dict): This is a data dictionary with the same structure as the experimental config.

    Returns:
        ExperimentalConfig: The experimental config restructured to a pydantic model structure.
    """
    return ExperimentalConfig.model_validate(config_dict)
