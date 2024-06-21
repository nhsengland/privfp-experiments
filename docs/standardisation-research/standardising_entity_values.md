# Standardising Entity Types and their Values

This [GitHub repository](https://github.com/kaisugi/entity-related-papers?tab=readme-ov-file) posts a lot of material related to named-entity-recognition including methodologies for disambiguation and linking.

## Preprocessing Entity Values

### General NLP Cleaning
- **Lowercasing**
- **Removing Punctuation**
- **Spell Correction**
    - **[PySpellChecker](https://pypi.org/project/pyspellchecker/)**: Uses a Levenshtein Distance algorithm to find permutations within an edit distance of 2 from the original word.
    - **[TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html#spelling-correction)**: Spelling correction is based on Peter Norvig’s “How to Write a Spelling Corrector” as implemented in the pattern library. It is about 70% accurate.
    - **[autocorrect](https://github.com/filyp/autocorrect)**: Also based on Peter Norvig's work.
    
### Expanding Acronyms
- **[Ab3P](https://github.com/ncbi-nlp/Ab3P)**: Biomedical Specific acronym expansion tool trained on PubMed Abstracts.
- **[Spacy AbbrX](https://github.com/erre-quadro/spikex)**: Uses pre-trained spacy models to expand acronyms.

### Coreference Resolution
Implemented in the Neo4j pipeline, it involves replacing all pronouns with the referenced entity, helping resolve relationships between entities.

### Expanding Specific Entity Types

#### Expanding Names
- **[Probable People](https://github.com/datamade/probablepeople)**: Library for parsing and formatting person names.
- **[Python Nameparser](https://github.com/derek73/python-nameparser)**: An alternative library for parsing human names.
- **[Nominally](https://github.com/vaneseltine/nominally)**: Another tool for parsing names.

#### Expanding Location
- **[LibPostal](https://github.com/openvenues/libpostal)**: Library for parsing and formatting postal addresses.

### Formatting Entity Types

#### Dates
- **[DateParser](https://dateparser.readthedocs.io/en/latest/)**: Parses dates into the same format.
- **[Microsoft Recognizers-Text](https://github.com/microsoft/Recognizers-Text/tree/master/Python)**: Open-source and can be used locally. Supports multiple languages and various data types as detailed on their GitHub repo readme.

#### Phrases based on Context
- **[ExtEnD (Extractive Entity Disambiguation)](https://github.com/SapienzaNLP/extend)**: Can be integrated with the spacy framework to extend meanings of words using surrounding context.

## Resolving Entity Values

### Entity Disambiguation and Entity Linking

Wikification

- **[REL (Radboud Entity Linker)](https://github.com/informagi/REL)**: Uses the English Wikipedia as a knowledge source. Maps entities to Wikipedia IDs and normalizes outputs.

- **[Wikimapper](https://pypi.org/project/wikimapper/)**: Small Python library that maps Wikipedia page titles.

- **[spacy_entity_linker](https://huggingface.co/MartinoMensio/spaCy-entity-linker)**: Uses a knowledge base (Wikipedia) to find similar entities.

- **[Neo4J (uses Bloom)](https://github.com/neo4j-graph-examples/entity-resolution)**: Resolves entities.

- **[BLINK](https://github.com/facebookresearch/BLINK)**: Facebook's architecture for linking entities to Wikipedia.

- **[SpacyFishing](https://github.com/Lucaterre/spacyfishing)**: Framework to fetch wiki IDs for extracted entity values.

- **[BENT](https://github.com/lasigeBioTM/BENT/tree/main?tab=readme-ov-file#readme)**: Open-source repo aimed at resolving entity ambiguity and linking for biomedical terms.

### Entity Embedding-based Normalisation Approaches
- **[Entity Embed](https://github.com/vintasoftware/entity-embed?tab=readme-ov-file)**: A PyTorch library for embedding entities into vectors to support scalable record linkage and entity resolution.
- **[StarSpace](https://github.com/facebookresearch/StarSpace)**: Facebook tool for embedding entities and link prediction in knowledge bases.
- **[Spacy Dependency Parser](https://spacy.io/usage/linguistic-features#dependency-parse)**: Extracts nouns from text, uses knowledge bases, and derives roots from texts.

### Medical Code Resolution
- **[ICD10cm Augmented](https://nlp.johnsnowlabs.com/2021/11/01/sbiobertresolve_icd10cm_augmented_billable_hcc_en.html)**: John Snow Labs tool for resolving clinical text using ICD-10 codes.
- **[Healthcare Relation Extraction](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/healthcare/relation_extraction/overview_relation.ipynb)**: Notebook demonstrating relation extraction in healthcare data using John Snow Labs tools with ICD-10 codes.
- **[SNOMED CT Entity Linking Challenge](https://github.com/drivendataorg/snomed-ct-entity-linking)**: Competition for linking text spans in clinical notes with specific topics in the SNOMED CT clinical terminology.

### String Comparisons between Entities
- **[Jellyfish](https://github.com/jamesturk/jellyfish)**: Library for approximate and phonetic matching of strings.
- **[PyStringMatching](https://github.com/anhaidgroup/py_stringmatching)**: Library for string matching.
- **[TextDistance](https://github.com/life4/textdistance)**: Library for measuring text similarity.
- **[StringCompare](https://github.com/OlivierBinette/StringCompare)**: Library for comparing string structures.
- **[Abydos](https://github.com/chrislit/abydos)**: Supports phonetic algorithms, string distance metrics, stemmers, and string fingerprints.
- **[FuzzyWuzzy](https://pypi.org/project/fuzzywuzzy/)**: Uses Levenshtein distance to identify close strings.

## Research Paper Concepts
- **[BIOSYN with Synonym Marginalisation](https://arxiv.org/pdf/2005.00239)**: Method and framework to train and identify synonyms in biomedical text.
- **[Text Normalization Using Encoder–Decoder Networks Based on the Causal Feature Extractor](https://www.mdpi.com/2076-3417/10/13/4551)**: Research on text normalization.
- **[EL-Chatbot](https://aclanthology.org/2024.lrec-main.275/)**: Paper outlining entity linking using a chatbot, with an associated GitHub repo.
