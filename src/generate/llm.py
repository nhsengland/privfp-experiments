from .config import path_synthea_output, path_llm_output
from .utils import load_synthea_output, save
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import json


def run(model, template):
    batch = load_synthea_output(path_synthea_output)

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = Ollama(model=model, callback_manager=callback_manager)
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm

    results = chain.batch(batch)
    data = json.dumps(results)
    save(path_llm_output, data)
