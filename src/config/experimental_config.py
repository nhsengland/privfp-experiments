from pydantic import BaseModel
import yaml
from typing import Dict, Optional, List


class LocalFeaturesConfig(BaseModel):
    hf_repo_id: Optional[str] = None
    hf_filename: Optional[str] = None
    prompt_template_path: Optional[str] = None


class OllamaFeaturesConfig(BaseModel):
    ollama_ner_model: Optional[str] = None
    prompt_template_path: Optional[str] = None


class GenerateModelFeaturesConfig(BaseModel):
    llm_model_name: str
    prompt_template_path: str


class ExtractionConfig(BaseModel):
    server_model_type: str
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


class ExperimentalConfig(BaseModel):
    outputs: OutputsConfig
    synthea: SyntheaConfig
    generate: GenerateConfig
    extraction: ExtractionConfig


def load_experimental_config() -> ExperimentalConfig:
    with open("../config/experimental_config.yaml", "r") as config_file:
        config_dict = yaml.safe_load(config_file)
        return ExperimentalConfig.model_validate(config_dict)


def reload_as_experimental_config(config_dict: dict) -> ExperimentalConfig:
    return ExperimentalConfig.model_validate(config_dict)
