# Large Language Models

!!! warning

    Requires [Ollama](https://github.com/ollama/ollama) to run. This particular setup was tested with [Ollama version 0.1.27](https://ollama.com/download) on an M1 MBP.

[Ollama](https://github.com/ollama/ollama) is used for the unstructured generative component of Privacy Fingerprint. It provides a simple interface to download quantised models and run inference locally.

## Start Ollama

Either open up the desktop application or a terminal and enter `ollama serve`.

## Ollama models

To download a model open a terminal and enter `ollama pull <model_name>`. The example notebooks in this repository currently use `llama2:latest fe938a131f40`.

See the [Ollama model library](https://ollama.com/library) for all available models.

## Other models

It is possible to use your own models not specified in the Ollama model library. Ollama supports the `.gguf` format and many quantised and non-quantised models can be found on the [Hugging Face Hub](https://huggingface.co/models).

To quantise a model, check out the resources on [setting up open source LLMs](../open-source-llm-exploration/setup.md) with [llama.cpp](https://github.com/ggerganov/llama.cpp) and the introductory reading around quantisation.