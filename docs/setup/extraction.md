# Entity extraction

!!! warning

    Requires the quantised `NER/UniNER-7B-type` model placed in the `model` folder.

The quantised model was created by cloning the [llama.cpp](https://github.com/ggerganov/llama.cpp) repository and quantising the `Universal-NER/UniNER-7B-type` locally to `q4_1.gguf` format.

The [llama.cpp](https://github.com/ggerganov/llama.cpp) repository has guidance on their repo in their Prepare and Quantize section. Alternatively there is a medium article that goes through all of this in a step-by-step process.

For more information on quantising see [here](../open-source-llm-exploration/setup.md).