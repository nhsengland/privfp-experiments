from .utils import load_output_synthea
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import json


def run(model, template, input=None, load_file=False):
    if input is None and not load_file:
        print("Either input or load_file must be provided.")
        return

    elif input is not None and load_file:
        print("Both input and load_file cannot be provided at the same time.")
        return

    batch = load_output_synthea(input, load_file)

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = Ollama(model=model, callback_manager=callback_manager)
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm

    results = chain.batch(batch)
    output = json.dumps(results)

    return output
