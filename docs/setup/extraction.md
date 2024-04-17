# Install UniversalNER Locally

!!! warning

    Requires the quantised `NER/UniNER-7B-type` model placed in the `model` folder.

## Downloading a Quantised version of the model from HuggingFace

This HuggingFace [repository](https://huggingface.co/yuuko-eth/UniNER-7B-all-GGUF/tree/main) holds a range of quantized UniversalNER Models. Any of these models can be downloaded, but make sure you download a model that your RAM can handle.

``` shell title="Download the smallest Quantised UniversalNER model from Huggingface"
cd privfp-experiments
source .venv/bin/activate
huggingface-cli download yuuko-eth/UniNER-7B-all-GGUF UniversalNER-7B-all-Q4_0.gguf --local-dir ./models
```
!!! warning

    You may need to change the universal_ner_path set in the ./src/config.py file.

## Quantising the UniversalNER model yourself
The quantised model was created by cloning the [llama.cpp](https://github.com/ggerganov/llama.cpp) repository and quantising the `Universal-NER/UniNER-7B-type` locally to `q4_1.gguf` format.

First you need to install the llama.cpp repo. You need to run the MAKE command to create essential directories.
``` shell title="Installing the Llama.cpp repo"
git clone llama.cpp
cd llama.cpp
MAKE # If you got CPU 
MAKE CUBLAS=1 # If you got GPU
```

In the llamma.cpp repo you will need to create a python environment to install all the necessary requirements
``` shell title="Creating a Python Environment for the Llama Repository"
cd llama.cpp
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Next you need to download the UniversalNER model.
``` shell title="Download UniversalNER from HuggingFace"
pip install transformers datasets sentencepiece
huggingface-cli download Universal-NER/UniNER-7B-type --local-dir models
```

Next you will convert the model into a 32 floating point size.
``` shell title="Convert UniversalNER model to f32 accuracy"
python convert.py ./models
```

Then you convert the f32 point to a q4_1 bit of accuracy.
``` shell title="Converting UniversalNER f32 to q4_1 accuracy"
./quantize models/ggml-model-f32.gguf models/quantized_q4_1.gguf q4_1
```

This quantized model is located in the quantize models folders. This model can then be transderred to our repo's ./model folder.

The steps provided above have been retrieved from a [medium article](https://medium.com/vendi-ai/efficiently-run-your-fine-tuned-llm-locally-using-llama-cpp-66e2a7c51300) 
