from ..utils import load_json_from_path_or_variable, save_json, load_json

import json
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any, Union


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


class GenerateLLM:
    """
    Class for generating language model outputs based on Synthea data.

    Methods:
        run: Generate language model outputs based on Synthea data.
        load: Load previously generated language model outputs from file.
    """

    def __init__(
        self,
        synthea_input: Union[str, List[Dict[str, Any]]] = None,
        synthea_path: str = None,
        save_output: bool = False,
        path_output: str = None,
    ) -> None:
        """
        Initializes GenerateLLM object.

        Args:
            synthea_input (List[Dict[str, Any]]): Synthea output data or variable name containing Synthea output data.
            synthea_path (str): File path to load Synthea output data from.
            save_output (bool): Whether to save the output to a file.
            path_output (str): Path to the output file.
        """
        self.synthea_input = synthea_input
        self.synthea_path = synthea_path
        self.save_output = save_output
        self.path_output = path_output

    def run(
        self, model: Any, template: str, verbose: bool = True
    ) -> List[str]:
        """
        Generate synthetic medical notes from Synthea data.

        Args:
            model (Any): Language model to use for generation.
            template (str): Template for language model prompts.
            verbose (bool): Decides whether verbose is true or false.

        Returns:
            List[str]: Generated a list of synthetic medical notes.
        """

        batch = get_batch(self.synthea_input, self.synthea_path)

        callback_manager = CallbackManager([])

        if verbose:
            callback_manager.add_handler(StreamingStdOutCallbackHandler())

        llm = Ollama(model=model, callback_manager=callback_manager)

        prompt = PromptTemplate.from_template(template)
        chain = prompt | llm

        results = chain.batch(batch)

        if self.save_output:
            save_json(results, self.path_output)

        return results

    def load(self) -> List[str]:
        """
        Load previously generated language model outputs from file.

        Returns:
            List[str]: Loaded language model outputs.
        """
        output = load_json(self.path_output)
        return output
