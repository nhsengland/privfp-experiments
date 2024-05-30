import copy
import itertools
import json
import os
from omegaconf import OmegaConf
from typing import List, Tuple, Any, Dict, Union

from src.config.experimental_config import (
    load_experimental_config,
    reload_as_experimental_config,
    ExperimentalConfig,
    SyntheaConfig,
    GenerateConfig,
    ExtractionConfig,
)
from src.generate.synthea import GenerateSynthea
from src.generate.llm import GenerateLLM
from src.extraction.extraction import Extraction
from src.config.global_config import load_global_config
from src.config.experimental_config_visualisation import draw_dag_graph

from src.utils import load_json


class ExperimentalConfigHandler:
    def __init__(
        self,
        default_config_path: str,
        iter_overrides: dict = dict(),
        combine_overrides: dict = dict(),
    ):
        """
        Initialize the ExperimentalConfigHandler.

        Args:
            default_config_path (str): This defines the location of the default experimental config path.
            iter_overrides (dict, optional): Overrides to define to override each experimental config. Defaults to dict().
            combine_overrides (dict, optional): Configuration to combine before iterating across the config. Defaults to dict().
        """
        self.iter_overrides = iter_overrides
        self.combine_overrides = combine_overrides

        global_config = load_global_config()
        experiment_name = self.iter_overrides["outputs.experiment_name"]
        experiment_path = (
            f"{global_config.output_paths.output_folder}/{experiment_name}"
        )

        self.experiment_dir_path = experiment_path

        # create the experiment config path
        experiment_config_filename = default_config_path.split("/")[-1]
        self.experiment_config_path = (
            f"{experiment_path}/{experiment_config_filename}"
        )

        move_experiment_config_if_not_exists(
            experiment_config_path=self.experiment_config_path,
            default_config_path=default_config_path,
        )

        # Move experimental config file to experiment folder if file doesnt exist.
        self.experimental_configs, self.output_path = (
            self.create_experimental_config_list()
        )

    def create_experimental_config_list(
        self,
    ) -> Dict[
        str, List[Union[SyntheaConfig, GenerateConfig, ExtractionConfig]]
    ]:
        """
        Create a dictionary which holds all the unique configuration you need to run at each point.

        Returns:
            Dict[str, List[Union(SyntheaConfig, GenerateConfig, ExtractionConfig)]]
        """
        experimental_configs, output_path = generate_experimental_config_list(
            experiment_dir_path=self.experiment_dir_path,
            experiment_config_path=self.experiment_config_path,
            iter_overrides=self.iter_overrides,
            combine_overrides=self.combine_overrides,
        )

        synthea_list = list()
        generate_list = list()
        extraction_list = list()

        for config in experimental_configs:
            synthea_list.append(config.synthea)
            generate_list.append(config.generate)
            extraction_list.append(config.extraction)

        experimental_config_dict = {
            "synthea": remove_duplicates(synthea_list, SyntheaConfig),
            "generate": remove_duplicates(generate_list, GenerateConfig),
            "extraction": remove_duplicates(extraction_list, ExtractionConfig),
        }
        self.experimental_configs = (
            experimental_config_dict  # Update experimental_configs attribute
        )
        return experimental_config_dict, output_path

    def load_component_experimental_config(
        self, component_type: str
    ) -> List[Union[SyntheaConfig, GenerateConfig, ExtractionConfig]]:
        """
        Load experimental configs based on the specified component type.

        Args:
            component_type (str): The type of component to load.

        Returns:
            List[Union[SyntheaConfig, GenerateConfig, ExtractionConfig]]: List of experimental configs of the specified component type.
        """
        if component_type == "synthea":
            return self.experimental_configs["synthea"]
        elif component_type == "generate":
            return self.experimental_configs["generate"]
        elif component_type == "extraction":
            return self.experimental_configs["extraction"]
        else:
            raise ValueError(
                "Invalid component type. Must be synthea, generate, or extraction."
            )

    def run_component_experiment_config(self, component_type: str) -> None:

        if component_type == "synthea":
            ComponentClass = GenerateSynthea
        elif component_type == "generate":
            ComponentClass = GenerateLLM
        elif component_type == "extraction":
            ComponentClass = Extraction

        for i, component_config in enumerate(
            self.load_component_experimental_config(component_type)
        ):
            print(f"{component_type} run {i} with config {component_config}")
            component_output = ComponentClass(component_config).run_or_load()
            print(component_output, "\n")
        pass

    def update_iter_overrides(self, new_iter_overrides: dict):
        """
        Update the iter_overrides with new values. If a key already exists, append the value to a list.

        Args:
            new_iter_overrides (dict): New iter_overrides to update.
        """
        for key, value in new_iter_overrides.items():
            if key in self.iter_overrides:
                if isinstance(self.iter_overrides[key], list):
                    self.iter_overrides[key].append(value)
                else:
                    self.iter_overrides[key] = [
                        self.iter_overrides[key],
                        value,
                    ]
            else:
                self.iter_overrides[key] = value
        self.create_experimental_config_list()  # Update experimental config after updating iter_overrides

    def update_combine_overrides(self, new_combine_overrides: dict):
        """
        Update the combine_overrides with new values. If a key already exists, append the value to a list.

        Args:
            new_combine_overrides (dict): New combine_overrides to update.
        """
        for key, value in new_combine_overrides.items():
            if key in self.combine_overrides:
                if isinstance(self.combine_overrides[key], list):
                    self.combine_overrides[key].append(value)
                else:
                    self.combine_overrides[key] = [
                        self.combine_overrides[key],
                        value,
                    ]
            else:
                self.combine_overrides[key] = value
        self.create_experimental_config_list()  # Update experimental config after updating combine_overrides

    def load_pipeline_visualisation(self):
        """This creates a unidirectional DAG that shows the experimental workflow."""

        draw_dag_graph(config_handler=self, path_outputs=self.output_path)

    def load_specified_data_file(self, filename: str) -> Dict[str, Any]:
        """Loads data file that is labelled on the experimental pipeline dag visualisation.

        Args:
            filename (str): This is the name of the file without the extension. i.e. you would say generate_0 not generate_0.json

        Returns:
            (Dict[str, Any]): This returns a dictionary that was created from this step.
        """

        component_type = filename.split("_")[0]
        filename_path = (
            f"{self.experiment_dir_path}/{component_type}/{filename}.json"
        )

        data_output = load_json(path=filename_path)

        return data_output


def get_nested_keys_with_list(dictionary: dict):
    """
    Recursively construct a nested list of keys corresponding to nested dictionaries with list values.

    Args:
        dictionary (dict): The dictionary to traverse over.

    Returns:
        list: Nested list of keys for dictionaries with list values.
    """
    keys = []

    nested_list = []
    for key, value in dictionary.items():
        current_keys = keys + [key]
        if isinstance(value, dict):
            # If the value is a dictionary, recursively call the function
            nested_sublist = get_nested_keys_with_list(value, current_keys)
            if nested_sublist:
                # If the nested dictionary contains lists, append the current keys
                nested_list.extend(nested_sublist)
        elif isinstance(value, list):
            # If the value is a list, append the current keys
            nested_list.append(current_keys)

    return nested_list


def verify_keys_exist(config: ExperimentalConfig, overrides: dict):
    """
    Verify that keys in the dictionaries exist in the config.

    Args:
        config (ExperimentalConfig): The experimental pydantic config.
        overrides (dict): Dictionary of keys to iterate over.

    Raises:
        KeyError: If any key does not exist in the config.

    """
    for key, values in overrides.items():
        current_dict = config.model_dump()
        for subkey in key.split("."):
            if subkey in current_dict:
                current_dict = current_dict[subkey]
            else:
                raise KeyError(
                    f"The key '{subkey}' does not exist in the config."
                )


def verify_same_count(combine_overrides: dict):
    """
    Verify that keys that group together from their top level have the same count of items in their list.

    Args:
        combine_overrides (dict): Dictionary of keys to combine.

    Raises:
        ValueError: If keys that group together do not have the same count of items in their list.
    """
    group_counts = {}
    for key, values in combine_overrides.items():
        top_level_key = ".".join(key.split(".")[:-1])
        if top_level_key in group_counts:
            if group_counts[top_level_key] != len(values):
                raise ValueError(
                    f"The keys '{top_level_key}' do not have the same count of items in their list."
                )
        else:
            group_counts[top_level_key] = len(values)


def get_combination_overrides(combine_overrides: dict) -> List[dict]:
    """
    Creates a list of dictionaries to be combined from the combine_overrides.

    Args:
        combine_overrides (dict): This is a combine dictionary override which is a dictionary with keys corresponding to the experiment config.

    Returns:
        List[Tuple[dict]]: A List of dictionaries to be combined based on the combine_overrides given.

    """
    update_combine_config = []

    # Iterate over unique top-level keys
    for top_level_key in set(key.split(".")[0] for key in combine_overrides):
        top_level_override = {
            k: v
            for k, v in combine_overrides.items()
            if k.startswith(top_level_key)
        }
        # Counts how deeply nested a value, which is a list, for a given key.
        top_level_count = len(next(iter(top_level_override.values()), []))

        # Iterate over the indices of the top-level count
        for i in range(top_level_count):
            # Construct dictionary for current index
            add_dict = {}
            for k, v in top_level_override.items():
                if isinstance(v, list):
                    add_dict[k] = v[i]
                else:
                    add_dict[k] = v
            update_combine_config.append(add_dict)

    return update_combine_config


def combine_list_of_dictionaries(iter_comb: List[Tuple[dict]]) -> List[dict]:
    """
    Combine a list of dictionaries

    Args:
        iter_comb (list): A list of tuple dictionaries to be combined, where each dictionary only has one key - value pair.

    Returns:
        List[dict]: A list of combine dictionaries from each of the dictionaries that existed in the tuple.

    """
    combined_dicts = []
    for items in iter_comb:
        combined_dict = {}
        for item in items:
            combined_dict.update(item)
        combined_dicts.append(combined_dict)
    return combined_dicts


def get_iter_overrides(iter_overrides: dict) -> List[dict]:
    """
    Generate combinations of overrides from a dictionary.

    Args:
        iter_overrides (dict): A dictionary containing override values.

    Returns:
        list: A list of dictionaries representing combinations of override values.

    """
    update_iter_config = []

    for key, value in iter_overrides.items():
        if isinstance(value, list):
            inside_list = [{key: v} for v in value]
            update_iter_config.append(inside_list)
        else:
            update_iter_config.append([{key: value}])

    iter_comb = list(itertools.product(*update_iter_config))

    combined_dicts = combine_list_of_dictionaries(iter_comb)

    return combined_dicts


def create_total_combined_overrides(
    experimental_config_path: str,
    iter_overrides: dict,
    combine_overrides: dict,
) -> List[dict]:
    """
    Generate total combined overrides by combining iteration and combination overrides.

    Args:
        experimental_config_path (str): The path of where the experimental config is located.
        iter_overrides (dict): A dictionary containing iteration overrides.
        combine_overrides (dict): A dictionary containing combination overrides.

    Returns:
        List[dict]: A list of dictionaries representing total combined overrides.

    """

    experimental_config = load_experimental_config(experimental_config_path)

    # Verify configs have the correct inputs requireed.
    verify_keys_exist(experimental_config, combine_overrides)
    verify_same_count(combine_overrides)

    # Creates a list of dictionaries to be combined from each overide type.
    comb_list = get_combination_overrides(combine_overrides)
    iter_list = get_iter_overrides(iter_overrides)

    if len(comb_list) == 0:
        total_comb = iter_list
    elif len(iter_list) == 0:
        total_comb = comb_list
    else:
        total_comb = list(itertools.product(*[iter_list, comb_list]))
        total_comb = combine_list_of_dictionaries(total_comb)

    clean_comb = correct_overrides_model_serving_type(total_comb)
    return clean_comb


def correct_overrides_model_serving_type(
    total_overrides: List[dict],
) -> List[dict]:
    """Function to correct for instances where you want to try various model_serving types with different values, but don't want complete iteration being copied.

    Args:
        total_overrides (List[dict]): List of total overrides you want to overwrite.

    Returns:
        List[dict]: Returns a list of ovverrides where None has been forced for some specific serving model vqriables.
    """
    configurations = copy.deepcopy(total_overrides)
    for config in configurations:
        if "extraction.server_model_type" in config.keys():
            if config["extraction.server_model_type"] != "gliner":
                config["extraction.gliner_features.gliner_model"] = None
            if config["extraction.server_model_type"] != "ollama":
                config["extraction.ollama_features.ollama_ner_model"] = None
                config["extraction.ollama_features.prompt_template_path"] = (
                    None
                )
            if config["extraction.server_model_type"] != "local":
                config["extraction.local_features.hf_repo_id"] = None
                config["extraction.local_features.hf_filename"] = None
                config["extraction.local_features.prompt_template_path"] = None

    return configurations


def create_paths_per_component_per_override(
    sub_override: dict,
) -> List[List[str]]:
    """
    Generate paths per component per override.

    Args:
        sub_override (dict): A dictionary containing an override dictionary for a specific combinations.

    Returns:
        List[List[str]]: A list containing paths per component per override.

    """
    synthea_features = get_component_features(
        sub_override, component_type="synthea"
    )
    generate_features = get_component_features(
        sub_override, component_type="generate"
    )
    extraction_features = get_component_features(
        sub_override, component_type="extraction"
    )

    synthea_paths = [synthea_features] if synthea_features else []
    generate_paths = (
        [synthea_features + "_" + generate_features]
        if generate_features
        else []
    )
    extraction_paths = (
        [
            synthea_features
            + "_"
            + generate_features
            + "_"
            + extraction_features
        ]
        if extraction_features
        else []
    )

    past_data_path = ["" if synthea_paths else "default"]

    synthea_paths = add_path_or_carry_through(
        past_data_paths=past_data_path, data_paths=synthea_paths
    )
    generate_paths = add_path_or_carry_through(
        past_data_paths=synthea_paths, data_paths=generate_paths
    )
    extraction_paths = add_path_or_carry_through(
        past_data_paths=generate_paths, data_paths=extraction_paths
    )

    return synthea_paths, generate_paths, extraction_paths


def get_component_features(overrides: dict, component_type: str) -> List[str]:
    """
    Extract component features based on component type from the given overrides.

    Args:
        overrides (dict): A dictionary containing override values.
        component_type (str): The type of component to extract features for.

    Returns:
        List[str]: A list of strings representing the extracted component features.
    """
    component_list = [
        f"{'_'.join(key.split('.')[1:])}_{value}"
        for key, value in overrides.items()
        if key.startswith(component_type)
    ]
    component_features = "_".join(component_list + [component_type])
    return component_features


def add_path_or_carry_through(
    data_paths: List[str], past_data_paths: List[str]
) -> List[str]:
    """
    Add paths or carry through existing paths based on the presence of data paths.

    Args:
        data_paths (List[str]): A list of data paths to be added.
        past_data_paths (List[str]): A list of past data paths to be carried through if no data paths are present.

    Returns:
        List[str]: A list of data paths with added paths or carried-through past data paths.

    """
    if len(data_paths) == 0:
        for path in past_data_paths:
            data_paths.append(path)

    return data_paths


def get_important_key_values(dict: Dict, component_type: str):
    return {
        key: value
        for key, value in dict.items()
        if (key.startswith(component_type) and value is not None)
    }


def get_path_and_output_from_config(path_dict: Dict, file_prefix: str):

    path_dict = copy.deepcopy(path_dict)
    output_dict = dict()

    for i, path in enumerate(path_dict.keys()):
        value = path_dict[path]
        path_dict[path] = f"{file_prefix}_{i}.json"
        output_dict[f"{file_prefix}_{i}"] = value

    return path_dict, output_dict


def create_path_and_output_dict(synthea_dict, generate_dict, extraction_dict):

    global_config = load_global_config()
    synthea_path, synthea_output = get_path_and_output_from_config(
        synthea_dict, global_config.output_paths.synthea_prefix
    )
    generate_path, generate_output = get_path_and_output_from_config(
        generate_dict, global_config.output_paths.generate_prefix
    )
    extraction_path, extraction_output = get_path_and_output_from_config(
        extraction_dict, global_config.output_paths.extraction_prefix
    )

    combined_path = {**synthea_path, **generate_path, **extraction_path}
    combined_output = {
        **synthea_output,
        **generate_output,
        **extraction_output,
    }
    return combined_path, combined_output


def create_and_save_data_paths(total_combined_overrides: List[dict]) -> str:
    """
    Create and save data paths based on combined overrides.

    Args:
        total_combined_overrides (List[dict]): A list of dictionaries representing total combined overrides.

    Returns:
        str: The path where the data paths are saved.

    """

    synthea_dict = dict()
    generate_dict = dict()
    extraction_dict = dict()

    for sub_override in total_combined_overrides:
        synthea_paths, generate_paths, extraction_paths = (
            create_paths_per_component_per_override(sub_override)
        )

        synthea_values = get_important_key_values(
            sub_override, component_type="synthea"
        )
        generate_values = get_important_key_values(
            sub_override, component_type="generate"
        )
        extraction_values = get_important_key_values(
            sub_override, component_type="extraction"
        )

        synthea_dict[synthea_paths[0]] = synthea_values
        generate_dict[generate_paths[0]] = generate_values
        extraction_dict[extraction_paths[0]] = extraction_values

    path_dict, output_dict = create_path_and_output_dict(
        synthea_dict, generate_dict, extraction_dict
    )

    return path_dict, output_dict


def update_experimental_config_value(
    key_string: str, experimental_config: dict, new_value: Any
):
    """Updates experimental config with value defined by the overrides combination produced.

    Args:
        key_string (str): This is the location of the value being change in the overrides.
        experimental_config (dict): This is the config that you want to rewrite values over onto.
        new_value (Any): This is the new value you want to the specific key string value you want to overwrite.
    """

    keys = key_string.split(".")
    current_experiment = experimental_config
    for key in keys[:-1]:
        current_experiment = current_experiment[key]
    current_experiment[keys[-1]] = new_value


def create_override_experimental_config(
    experiment_dir_path: str,
    experiment_config_path: str,
    override: dict,
    data_paths: List[str],
) -> ExperimentalConfig:
    """
    Create an experimental configuration with overrides and data paths.

    Args:
        experiment_dir_path (str): A path to the location of where the experiment directory lives.
        experiment_config_path (str): A path to the location of where the experiment config sits.
        override (dict): A dictionary containing overrides to be applied to the experimental configuration.
        data_paths (List[str]): A list of data paths.

    Returns:
        ExperimentalConfig: The experimental configuration with applied overrides and data paths.

    """
    experimental_config = copy.deepcopy(
        load_experimental_config(experiment_config_path).model_dump()
    )
    global_config = load_global_config()

    for override_key, override_value in override.items():
        update_experimental_config_value(
            override_key, experimental_config, override_value
        )

    override_experiminetal_config = reload_as_experimental_config(
        experimental_config
    )

    synthea_paths, generate_paths, extraction_paths = (
        create_paths_per_component_per_override(override)
    )

    synthea_path = f"{experiment_dir_path}/{global_config.output_paths.synthea_prefix}/{data_paths[synthea_paths[0]]}"
    generate_path = f"{experiment_dir_path}/{global_config.output_paths.generate_prefix}/{data_paths[generate_paths[0]]}"
    extraction_path = f"{experiment_dir_path}/{global_config.output_paths.extraction_prefix}/{data_paths[extraction_paths[0]]}"

    override_experiminetal_config.synthea.path_output = synthea_path
    override_experiminetal_config.generate.synthea_path = synthea_path
    override_experiminetal_config.generate.path_output = generate_path
    override_experiminetal_config.extraction.llm_path = generate_path
    override_experiminetal_config.extraction.path_output = extraction_path

    return override_experiminetal_config


def generate_experimental_config_list(
    experiment_dir_path: str,
    experiment_config_path: str,
    iter_overrides: dict = dict(),
    combine_overrides: dict = dict(),
) -> List[ExperimentalConfig]:
    """
    Generate a list of experimental configurations based on iteration and combination overrides.

    Args:
        experiment_dir_path (str): path to where the experimental directory is located.
        experiment_config_path (str): path to where the experimental config sits.
        iter_overrides (dict, optional): A dictionary containing iteration overrides. Defaults to an empty dictionary.
        combine_overrides (dict, optional): A dictionary containing combination overrides. Defaults to an empty dictionary.

    Returns:
        List[ExperimentalConfig]: A list of experimental configurations.

    """
    total_combined_overrides = create_total_combined_overrides(
        experimental_config_path=experiment_config_path,
        iter_overrides=iter_overrides,
        combine_overrides=combine_overrides,
    )

    data_paths, output_paths = create_and_save_data_paths(
        total_combined_overrides
    )

    experimental_config_list = list()

    for i, override in enumerate(total_combined_overrides):
        override_config = create_override_experimental_config(
            experiment_dir_path=experiment_dir_path,
            experiment_config_path=experiment_config_path,
            override=override,
            data_paths=data_paths,
        )
        experimental_config_list.append(override_config)

    return experimental_config_list, output_paths


def get_unique_dicts(
    configurations: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Removes duplicate dictionaries from a list of dictionaries.

    Args:
        configurations (List[Dict[str, Any]]): List of dictionaries to be checked for duplicates.

    Returns:
        List[Dict[str, Any]]: List of unique dictionaries.
    """
    seen = set()
    result = []
    for d in configurations:
        # Convert dictionary to a string
        str_d = json.dumps(d, sort_keys=True)
        if str_d not in seen:
            seen.add(str_d)
            # Convert string back to dictionary
            result.append(json.loads(str_d))
    return result


def remove_duplicates(
    configurations: List[
        Union[SyntheaConfig, GenerateConfig, ExtractionConfig]
    ],
    pydantic_config: Union[SyntheaConfig, GenerateConfig, ExtractionConfig],
) -> List[Union[SyntheaConfig, GenerateConfig, ExtractionConfig]]:
    """
    Removes duplicate configurations based on their model dumps.

    Args:
        configurations (List[Union[SyntheaConfig, GenerateConfig, ExtractionConfig]]): List of configurations.
        pydantic_config (Union[SyntheaConfig, GenerateConfig, ExtractionConfig]): An instance of a Pydantic configuration model.

    Returns:
        List[Union[SyntheaConfig, GenerateConfig, ExtractionConfig]]: List of unique configurations.
    """
    # Convert models to dictionaries
    configuration_dicts = [config.model_dump() for config in configurations]

    # Get unique dictionaries
    unique_dicts = get_unique_dicts(configuration_dicts)

    # Convert unique dictionaries back to Pydantic models
    unique_configurations = [
        pydantic_config(**config) for config in unique_dicts
    ]

    return unique_configurations


def create_experimental_config_list(
    experiment_dir_path: str,
    iter_overrides: dict = dict(),
    combine_overrides: dict = dict(),
) -> Dict[str, List[Union[SyntheaConfig, GenerateConfig, ExtractionConfig]]]:
    """Create a dictionary which holds all the unique configuration you need to run at each point.

    Args:
        experiment_dir_path (str): This defines the path to the experiment directory.
        iter_overrides (dict, optional): This is the overrides you want to define to override each experimental config. Defaults to dict().
        combine_overrides (dict, optional): This is config you want to combine before iterating across the config. Defaults to dict().

    Returns:
        Dict[str, List[Union(SyntheaConfig, GenerateConfig, ExtractionConfig)]]
    """

    experimental_configs, output_path = generate_experimental_config_list(
        experiment_dir_path=experiment_dir_path,
        iter_overrides=iter_overrides,
        combine_overrides=combine_overrides,
    )

    synthea_list = list()
    generate_list = list()
    extraction_list = list()

    for config in experimental_configs:
        synthea_list.append(config.synthea)
        generate_list.append(config.generate)
        extraction_list.append(config.extraction)

    experimental_config_dict = {
        "synthea": remove_duplicates(synthea_list, SyntheaConfig),
        "generate": remove_duplicates(generate_list, GenerateConfig),
        "extraction": remove_duplicates(extraction_list, ExtractionConfig),
    }

    return experimental_config_dict, output_path


def move_experiment_config_if_not_exists(
    experiment_config_path: str, default_config_path: str
) -> None:
    """
    Save the experimental configuration to a specified path if the file does not already exist.

    Args:
        experiment_config_path (str): The path where the experimental configuration should be saved.
        default_config_path (str): The path to the default configuration file used to load the initial configuration.
    """
    if not os.path.exists(experiment_config_path):
        # Load the experimental configuration
        experiment_config = load_experimental_config(default_config_path)

        # Convert the Pydantic model to a dictionary
        model_dict = experiment_config.dict()

        # Convert the dictionary to an OmegaConf DictConfig
        config = OmegaConf.create(model_dict)

        # Save the DictConfig to a YAML file
        OmegaConf.save(config, experiment_config_path)
        print(f"Configuration saved to {experiment_config_path}")
    else:
        print(f"Configuration file already exists at {experiment_config_path}")
