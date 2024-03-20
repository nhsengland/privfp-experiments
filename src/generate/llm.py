from ..utils import load_json_from_path_or_variable, save_json, load_json

import json
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate


def get_batch(from_variable, from_path):

    data = load_json_from_path_or_variable(from_variable, from_path)

    batch = []

    for i in range(len(data)):
        batch.append({"data": json.dumps(data[i])})

    return batch


class GenerateLLM:
    def __init__(
        self,
        synthea_input=None,
        synthea_path=None,
        save_output=False,
        path_output=None,
    ):
        self.synthea_input = synthea_input
        self.synthea_path = synthea_path
        self.save_output = save_output
        self.path_output = path_output

    def run(self, model, template):

        batch = get_batch(self.synthea_input, self.synthea_path)

        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        llm = Ollama(model=model, callback_manager=callback_manager)

        prompt = PromptTemplate.from_template(template)
        chain = prompt | llm

        results = chain.batch(batch)

        if self.save_output:
            save_json(results, self.path_output)

        return results

    def load(self):
        output = load_json(self.path_output)
        return output
