from pydantic import BaseModel
import yaml
from typing import Dict


class OutputPath(BaseModel):
    output_folder: str
    extraction_template: str
    generate_template: str


class SyntheaPaths(BaseModel):
    path_synthea: str
    path_csv: str
    path_patients: str
    path_encounters: str


class GlobalConfig(BaseModel):
    output_path: OutputPath
    synthea_paths: SyntheaPaths


def load_global_config() -> GlobalConfig:
    with open("../config/global_config.yaml", "r") as config_file:
        config_dict = yaml.safe_load(config_file)
        return GlobalConfig.model_validate(config_dict)
