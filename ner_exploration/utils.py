import json
import torch
import transformers
 
with open('./data/llm_dataset.json') as f:
    data = json.load(f)

print(data)


model = transformers.AutoModel.from_pretrained(
    'numind/entity-recognition-general-sota-v1',
    output_hidden_states=True
)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    'numind/entity-recognition-general-sota-v1'
)

encoded_input = tokenizer(
    data,
    return_tensors='pt',
    padding=True,
    truncation=True
)
output = model(**encoded_input)

# for better quality
emb = torch.cat(
    (output.hidden_states[-1], output.hidden_states[-7]),
    dim=2
)