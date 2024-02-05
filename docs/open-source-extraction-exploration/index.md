# Open source Extraction Exploration

Once we have LLM-generated medical notes we then want to extract entities from these notes to then produce a privacy risk score. 

In previous work, [AWS Comprehend Medical](https://docs.aws.amazon.com/comprehend-medical/) was first used to extract entities from these medical notes. In this project we want to explore using open-source named-entity extraction methods that could be used instead of AWS Comprehend Medical.

Experiments and example notebooks for the **extraction** component of PrivFp are available in the [privfp-gen-experiments](https://github.com/nhsengland/privfp-gen-experiments/tree/main/notebooks/unstructured_to_structured_module/ner_exploration) repository.