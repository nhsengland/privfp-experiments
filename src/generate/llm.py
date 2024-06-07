from ..utils import load_json_from_path_or_variable, save_json, load_json

import json
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any, Union

from src.config.experimental_config import GenerateConfig
from src.config.prompt_template_handler import (
    load_and_validate_generate_prompt_template,
)
from src.utils import file_exists
from src.config.global_config import GlobalConfig


class GenerateLLM:
    """
    Class for generating language model outputs based on Synthea data.

    Methods:
        run_or_load: Generates or Loads a language model outputs based on Synthea data.
    """

    def __init__(
        self,
        global_config: GlobalConfig,
        generateconfig: GenerateConfig,
        synthea_input: Union[str, List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Initializes GenerateLLM object.

        Args:
            global_config (GlobalConfig): This is a pydantic typing model that contains configuration parameters from global config.
            generateconfig (GenerateConfig): A pydantic typed config model with values of llm_model_name,
                                             prompt_template_path, synthea_path, and path_output.
            synthea_input (List[Dict[str, Any]]): Synthea output data or variable name containing Synthea output data.
        """
        GenerateConfig.model_validate(generateconfig.model_dump())

        self.synthea_input = synthea_input
        self.llm_model_name = generateconfig.llm_model_features.llm_model_name
        self.synthea_path = generateconfig.synthea_path
        self.path_output = generateconfig.path_output

        full_template_path = f"{global_config.output_paths.generate_template}/{generateconfig.llm_model_features.prompt_template_path}"
        self.prompt_template = load_and_validate_generate_prompt_template(
            full_template_path
        )

    def run_or_load(
        self,
        verbose: bool = False,
        resave: bool = False,
        save: bool = True,
    ) -> List[str]:
        """
        Generate or Load synthetic medical notes from Synthea data.

        Args:
            verbose (bool): Decides whether verbose is true or false. Defaults to False.
            resave (bool): Decides whether to resave a model or not. Defaults to False.
            save (bool): Determines whether you want to save any files, if this is false it doesn't save any files. Defaults to True.

        Returns:
            List[str]: Generated a list of synthetic medical notes.
        """

        if file_exists(self.path_output) and resave is False:
            output = load_json(self.path_output)
        else:
            batch = get_batch(self.synthea_input, self.synthea_path)

            callback_manager = CallbackManager([])

            if verbose:
                callback_manager.add_handler(StreamingStdOutCallbackHandler())

            llm = Ollama(
                model=self.llm_model_name, callback_manager=callback_manager
            )

            prompt = PromptTemplate.from_template(self.prompt_template)
            chain = prompt | llm

            output = chain.batch(batch)

            if save:
                if resave or file_exists(self.path_output) is False:
                    save_json(output, self.path_output)

        return output


def get_batch(
    from_variable: List[Dict[str, Any]], from_path: str
) -> List[Dict[str, str]]:
    """
    Get batch data from a variable or a file path containing JSON data.

    Args:
        from_variable (List[Dict[str, Any]]): Synthea output data.
        from_path (str): File path to load Synthea from.

    Returns:
        List[Dict[str, str]]: Batch data with JSON strings.

    Example:
        >>> from my_module import get_batch
        >>> data = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
        >>> batch = get_batch(data, '/path/to/data.json')
    """

    data = load_json_from_path_or_variable(from_variable, from_path)

    batch = []

    for i in range(len(data)):
        batch.append({"data": json.dumps(data[i])})

    return batch
