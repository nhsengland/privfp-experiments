from ..utils import load_json

import json
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate


def get_batch(from_variable, from_path):
    data = load_json(from_variable, from_path)
    batch = []

    for i in range(len(data)):
        batch.append({"data": json.dumps(data[i])})

    return batch


def run(model, template, data_variable=False, data_path=False):
    batch = get_batch(data_variable, data_path)

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = Ollama(model=model, callback_manager=callback_manager)
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm

    results = chain.batch(batch)
    output = json.dumps(results)

    return output
