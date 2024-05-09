from pydantic import BaseModel
import yaml
from typing import Dict, Optional


class LocalFeaturesConfig(BaseModel):
    hf_repo_id: str
    hf_filename: str


class OllamaFeaturesConfig(BaseModel):
    ollama_ner_model: str


class ExtractionConfig(BaseModel):
    serving_model_type: str
    local_features: LocalFeaturesConfig
    ollama_features: OllamaFeaturesConfig
    prompt_template_path: str


class GenerateConfig(BaseModel):
    llm_model_name: str
    prompt_template_path: str


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
