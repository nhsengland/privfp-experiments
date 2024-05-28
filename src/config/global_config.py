import yaml

from pydantic import BaseModel


class OutputSettings(BaseModel):
    output_folder: str
    extraction_template: str
    generate_template: str
    synthea_prefix: str
    generate_prefix: str
    extraction_prefix: str
    standardise_prefix: str


class SyntheaSettings(BaseModel):
    path_synthea: str


class GlobalConfig(BaseModel):
    output_paths: OutputSettings
    synthea: SyntheaSettings


def load_global_config() -> GlobalConfig:
    """Loads the global config from the main config folder.

    Returns:
        GlobalConfig: Returns the loaded in yaml file with the global config path that has been predefined.
    """
    with open("../config/global_config.yaml", "r") as config_file:
        config_dict = yaml.safe_load(config_file)
        return GlobalConfig.model_validate(config_dict)
