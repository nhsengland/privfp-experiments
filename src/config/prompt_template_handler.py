import json
import os

from typing import Dict


class PromptTemplateError(Exception):
    pass


def load_and_validate_prompt_template(
    filename: str, required_placeholders: list
) -> Dict[str, str]:
    """
    Loads and validates a prompt template from a JSON file.

    Args:
        filename (str): The file path of the JSON file.
        required_placeholders (list): List of required placeholders.

    Returns:
        dict: The loaded template.

    Raises:
        PromptTemplateError: If required placeholders are missing in the template.
    """
    with open(filename, "r") as f:
        data = json.load(f)

    template = data.get("prompt_template", "")

    # Check if required placeholders are present in the template
    for placeholder in required_placeholders:
        if placeholder not in template:
            raise PromptTemplateError(
                f"Prompt template must contain '{placeholder}'."
            )

    return template


def load_and_validate_extraction_prompt_template(
    filename: str,
) -> Dict[str, str]:
    """
    Loads and validates an extraction prompt template from a JSON file.

    Args:
        filename (str): The file path of the JSON file.

    Returns:
        dict: The loaded template.

    Raises:
        PromptTemplateError: If required placeholders are missing in the template.
    """
    return load_and_validate_prompt_template(
        filename, ["input_text", "entity_name"]
    )


def load_and_validate_generate_prompt_template(
    filename: str,
) -> Dict[str, str]:
    """
    Loads and validates a generate prompt template from a JSON file.

    Args:
        filename (str): The file path of the JSON file.

    Returns:
        dict: The loaded template.

    Raises:
        PromptTemplateError: If required placeholders are missing in the template.
    """
    return load_and_validate_prompt_template(filename, ["data"])


def save_template_to_json(
    template_str: str, file_path: str, required_placeholders: list
):
    """
    Saves the provided template string to a JSON file.

    Args:
        template_str (str): The template string to be saved.
        file_path (str): The file path where the JSON file will be saved.
        required_placeholders (list): List of required placeholders.

    Raises:
        PromptTemplateError: If required placeholders are missing in the template.
    """
    # Check if required placeholders are present in the template
    for placeholder in required_placeholders:
        if placeholder not in template_str:
            raise PromptTemplateError(
                f"Template must contain '{placeholder}'."
            )

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Convert template to JSON format
    json_template = json.dumps({"prompt_template": template_str}, indent=2)

    # Save JSON template to a file
    with open(file_path, "w") as f:
        f.write(json_template)

    print(f"Template saved to '{file_path}'")


def save_extraction_template_to_json(template_str: str, file_path: str):
    """
    Saves the provided extraction template string to a JSON file.

    Args:
        template_str (str): The extraction template string to be saved.
        file_path (str): The file path where the JSON file will be saved.
    """
    required_placeholders = ["input_text", "entity_name"]
    save_template_to_json(template_str, file_path, required_placeholders)


def save_generate_template_to_json(template_str: str, file_path: str):
    """
    Saves the provided generate template string to a JSON file.

    Args:
        template_str (str): The generate template string to be saved.
        file_path (str): The file path where the JSON file will be saved.
    """
    required_placeholders = ["data"]
    save_template_to_json(template_str, file_path, required_placeholders)
