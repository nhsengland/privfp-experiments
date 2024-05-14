import copy
import itertools
from typing import List, Tuple, Any

from src.config.experimental_config import (
    load_experimental_config,
    reload_as_experimental_config,
    ExperimentalConfig,
)
from src.config.global_config import load_global_config
from src.utils import save_json, load_json


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
    iter_overrides: dict, combine_overrides: dict
) -> List[dict]:
    """
    Generate total combined overrides by combining iteration and combination overrides.

    Args:
        iter_overrides (dict): A dictionary containing iteration overrides.
        combine_overrides (dict): A dictionary containing combination overrides.

    Returns:
        List[dict]: A list of dictionaries representing total combined overrides.

    """

    experimental_config = load_experimental_config()

    # Verify configs have the correct inputs requireed.
    verify_keys_exist(experimental_config, combine_overrides)
    verify_same_count(combine_overrides)

    # Creates a list of dictionaries to be combined from each overide type.
    comb_list = get_combination_overrides(combine_overrides)
    iter_list = get_iter_overrides(iter_overrides)

    if len(comb_list) == 0:
        return iter_list
    elif len(iter_list) == 0:
        return comb_list
    else:
        total_comb = list(itertools.product(*[iter_list, comb_list]))
        total_combined_dicts = combine_list_of_dictionaries(total_comb)
        return total_combined_dicts


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


def create_and_save_data_paths(total_combined_overrides: List[dict]) -> str:
    """
    Create and save data paths based on combined overrides.

    Args:
        total_combined_overrides (List[dict]): A list of dictionaries representing total combined overrides.

    Returns:
        str: The path where the data paths are saved.

    """
    global_config = load_global_config()

    total_synthea_paths = []
    total_generate_paths = []
    total_extraction_paths = []

    for sub_override in total_combined_overrides:
        synthea_paths, generate_paths, extraction_paths = (
            create_paths_per_component_per_override(sub_override)
        )

        total_synthea_paths.extend(synthea_paths)
        total_generate_paths.extend(generate_paths)
        total_extraction_paths.extend(extraction_paths)

    total_synthea_paths = list(set(total_synthea_paths))
    total_generate_paths = list(set(total_generate_paths))
    total_extraction_paths = list(set(total_extraction_paths))

    data_paths = {}

    for i, path in enumerate(total_synthea_paths):
        data_paths[path] = (
            f"{global_config.output_paths.synthea_prefix}_{i}.json"
        )

    for i, path in enumerate(total_generate_paths):
        data_paths[path] = (
            f"{global_config.output_paths.generate_prefix}_{i}.json"
        )

    for i, path in enumerate(total_extraction_paths):
        data_paths[path] = (
            f"{global_config.output_paths.extraction_prefix}_{i}.json"
        )

    experiment_name = total_combined_overrides[0]["outputs.experiment_name"]

    output_path = f"{global_config.output_paths.output_folder}/{experiment_name}/data_paths.json"
    save_json(data=data_paths, path=output_path)
    return output_path


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
    override: dict, data_paths: List[str]
) -> ExperimentalConfig:
    """
    Create an experimental configuration with overrides and data paths.

    Args:
        override (dict): A dictionary containing overrides to be applied to the experimental configuration.
        data_paths (List[str]): A list of data paths.

    Returns:
        ExperimentalConfig: The experimental configuration with applied overrides and data paths.

    """
    experimental_config = copy.deepcopy(
        load_experimental_config().model_dump()
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
    synthea_path = f"{global_config.output_paths.output_folder}/{global_config.output_paths.synthea_prefix}/{data_paths[synthea_paths[0]]}"
    generate_path = f"{global_config.output_paths.output_folder}/{global_config.output_paths.synthea_prefix}/{data_paths[generate_paths[0]]}"
    extraction_path = f"{global_config.output_paths.output_folder}/{global_config.output_paths.synthea_prefix}/{data_paths[extraction_paths[0]]}"

    override_experiminetal_config.synthea.path_output = synthea_path
    override_experiminetal_config.generate.synthea_path = synthea_path
    override_experiminetal_config.generate.path_output = generate_path
    override_experiminetal_config.extraction.llm_path = generate_path
    override_experiminetal_config.extraction.path_output = extraction_path

    return override_experiminetal_config


def generate_experimental_config_list(
    iter_overrides: dict = dict(), combine_overrides: dict = dict()
) -> List[ExperimentalConfig]:
    """
    Generate a list of experimental configurations based on iteration and combination overrides.

    Args:
        iter_overrides (dict, optional): A dictionary containing iteration overrides. Defaults to an empty dictionary.
        combine_overrides (dict, optional): A dictionary containing combination overrides. Defaults to an empty dictionary.

    Returns:
        List[ExperimentalConfig]: A list of experimental configurations.

    """
    total_combined_overrides = create_total_combined_overrides(
        iter_overrides=iter_overrides, combine_overrides=combine_overrides
    )

    output_path = create_and_save_data_paths(total_combined_overrides)

    data_paths = load_json(output_path)

    experimental_config_list = list()

    for i, override in enumerate(total_combined_overrides):
        override_config = create_override_experimental_config(
            override, data_paths
        )
        experimental_config_list.append(override_config)

    return experimental_config_list
