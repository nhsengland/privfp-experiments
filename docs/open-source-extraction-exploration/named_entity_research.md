# Open-source Named-entity Recognition Models 

Named-entity Recognition (NER) models aim to label words/phrases in unstructured data as a classified entity.

## Named-entity Recognition Models

A set of experiments were conducted with a set of medical notes, and a spot-check was conducted to get a general idea of how each NER model performed.

!!! info "Open-source NER Models"

    === "Spacy and SciSpacy"

        [Spacy](https://pypi.org/project/spacy/) and [SciSpacy](https://pypi.org/project/scispacy/) have a set of pre-trained open-source NER models availible for use. 

        * **spacy/en_core_web_md** and **spacy/en_core_web_lg** have been trained OntoNotes 5, Clearnlp Constituient-to-Dependency Conversion, WordNet 3.0, and Explosion vectors, and labels entities such as DATE, EVENT, PERSON, TIME, WORK_OF_ART etc.
        * **scispacy/en_core_sci_md** have been trained on biomedical data with ~360k vocabulary and 50k word vectors. Same labelling entitiy convention as the **spacy/en_core_web_md** and **spacy/en_core_web_lg** models.
        * **scispcacy/en_core_sci_scibert** have been trained on ~785k vocabulary and allenai/scibert-base as the transformer model. Everything is labelled as ENTITY.
        

    === "UniversalNER"
        
        [UniversalNER](https://universal-ner.github.io/) has been trained on data that has been prompted by ChatGPT and has resulted in a dataset that comprises of 45,889 input-output pairs, encompassing 240,725 entities and 13,020 distinct entity types. 
        
        UniversalNER works a little different from other NER models, as you have to prompt the model which entity you would like to extract. 

        Therefore this makes the model very good at extracting more diverse entities. 

        There are two ways to prompt the model:

        * One is hosting UniversalNER locally, and then calling an API to extract the entities from this local server.[Example Notebook](https://github.com/nhsengland/privfp-gen-experiments/blob/main/notebooks/unstructured_to_structured_module/ner_exploration/uniNer_api.ipynb)
        * The other is to quantise the model, and then you can run this model locally.[Example Notebook](https://github.com/nhsengland/privfp-gen-experiments/blob/main/notebooks/unstructured_to_structured_module/ner_exploration/uniNer_quantised.ipynb)

    === "SpanMarkerNER"

        [SpanMarketNER](https://github.com/tomaarsen/SpanMarkerNER) have a large range of pre-trained open source NER models.

        * span-marker-bert-base-fewnerd-fine-super
        * span-marker-roberta-large-fewnerd-fine-super
        * span-marker-xlm-roberta-base-fewnerd-fine-super
        * span-marker-roberta-large-ontonotes5
        * span-marker-xlm-roberta-large-conll03
        * span-marker-xlm-roberta-large-conll03-doc-context

## Creating your own Entity-Labelled Dataset
It is also encouraged in the NER space to label your own data with entities you want to specify and then train a foundation model on this smaller dataset to then label the remaining datasets.

 * [Numind](https://www.numind.ai/blog/a-foundation-model-for-entity-recognition) is a powerful foundation model that can be trained on a smaller dataset than previous foundation models (RoBERTa etc.) on a range of datasets. 
 * [Prodiggy](https://spacy.io/universe/project/prodigy) is an annotation tool that has been designed in a way that makes it easy to share the workload of annotating documents, and also verify annotated documents.