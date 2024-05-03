from pydantic import BaseModel
import yaml
from typing import Dict, Optional


class Generate(BaseModel):
    model_name: str
    prompt_template_path: str


class Extraction(BaseModel):
    serving_model_type: str
    local_features: Dict[str, str]
    ollama_features: Dict[str, str]
    prompt_template_path: str


class ExperimentalConfig(BaseModel):
    experiment_name: str
    generate: Optional[Generate]
    extraction: Optional[Extraction]


def load_experimental_config() -> ExperimentalConfig:
    with open("../config/experimental_config.yaml", "r") as config_file:
        config_dict = yaml.safe_load(config_file)
        return ExperimentalConfig.model_validate(config_dict)
