# Standardising with Knowledge Graphs

## From Document to Knowledge Graph

### Entity Type - Entity Value Relationship Extraction

1. **[KG-Completion from the Graph4NLP codebase](https://graph4ai.github.io/graph4nlp/tutorial/knowledge_graph_completion.html)**

2. **[OpenNRE](https://github.com/thunlp/OpenNRE):** This is an open-source repository which is used to infer relations from a given sentence.

3. **[Zett](https://github.com/megagonlabs/zett):** This is a zero shot entity relation extraction repo where you give the structure you expect the relation to be in and then it extracts out the connecting values from the text.

4. **[GliREL](https://github.com/jackboyla/GLiREL):** You can define the connections between entities using "glirel labels" i.e. you could say diagnosis is "treated with" medication.

5. **[GoLLie](https://github.com/hitz-zentroa/GoLLIE/blob/main/notebooks/Named%20Entity%20Recognition.ipynb):** Zero-shot approach to extracting out entities, where you provide some general relations you expect to see and this can extract the relations between entities.

6. **Research Paper Concepts:**

    * **[Generative Type Oriented Named Entity Extraction](https://aclanthology.org/2024.lrec-main.1412/):** A research paper on a generative approach to named entity extraction.

    * **[Co-attention Network for Joint Entity and Relation Extraction](https://aclanthology.org/2024.lrec-main.255):** A research paper on using a co-attention network for joint entity and relation extraction, with provided code.


### Document to Triplets

1. **[Text2Graph](https://github.com/xyjigsaw/Text2Graph?tab=readme-ov-file):** This is a pre-trained model on HuggingFace that has been trained by ChatGPT to identify triplets in text.

2. **[REBEL](https://huggingface.co/Babelscape/rebel-large):** This is a pre-trained model on HuggingFace that extracts triplets out from text. (BERT-based model - you would be limited by 512 tokens.)

3. **[Joint Entity and Relation Extraction](https://ceur-ws.org/Vol-3479/paper10.pdf):** This is a paper outlining the creation of a medically-related dataset to help fine-tune the REBEL model to be better at extracting out medically-related entities.

4. **[OpenIE Standalone Github Repository](https://github.com/dair-iitd/OpenIE-standalone):** A repository for OpenIE, a tool that extracts entities and their relationships from text.

5. There is an annotation tool called **[RTE](https://abera87.github.io/annotate/)** which uses OpenIE to extract out triplets.

    * **[Online Tool](https://abera87.github.io/annotate/)**

    * **[Paper](https://arxiv.org/pdf/2108.08184)**


### Triplets to Graph

**Structure:**

1. **[NetworkX](https://networkx.org/):** Python package used to create graph data structures.

2. **[Graph-tools](https://pypi.org/project/graph-tools/):** Python package that provides a number of features for handling directed/undirected graphs and complex networks.


**Visualisations:**

1. **[GraphViz](https://graphviz.org/):** Python packages to visualise graphs.

2. **[PyVis](https://pyvis.readthedocs.io/en/latest/):** Python package to visualise graphs.

3. **[IGraph](https://python.igraph.org/en/stable/):** Python package to visualise graphs.


**Graph Databases:**

1. **[Neo4J](https://neo4j.com/):** Community Edition which is free, but commercialised would need to be payed for.

2. **[JanusGraph](https://github.com/JanusGraph/janusgraph):** Fully open-source under the Apache 2 license - but it only supports Linux, and data storage requires a cost-based platform.

3. **[ArangoDB](https://arangodb.com/):** Community Edition which is free, but commercialised would need to be payed for.

4. **[OrientDB](https://www.orientdb.org/):** Community Edition which is free, but commercialised would need to be payed for.


## Entity Resolution Pipelines

### Neo4j

1. **[Neo4j Entity Resolution Example](https://github.com/neo4j-graph-examples/entity-resolution):** A GitHub repository with examples of using Neo4j for entity resolution.

2. **[Neo4j Whitepaper on Graph Databases](https://neo4j.com/whitepapers/definitive-guide-graph-databases-rdbms-developer/):** A whitepaper explaining the use of graph databases like Neo4j for various applications, including entity resolution.

3. **Neo4j Pipeline:** Outlines a process entities can be resolved:
    * Coreference Resolution: Replacing all pronouns with the referenced entity.
    * NER: Extracting out the named entities from the text provided.
    * Entity Disambiguation and Entity Linking: i.e. you could use Wikipedia ID linking - which tries to resolve words that have similar meaning. ("Wikification")
    * Co-Occurrence Graphs: This is inferring relationships between a pair of entities based on their presence within a specified unit of text.
    * Relationship Extraction:
        * Rule-based extraction: use grammatical dependencies to extract relationships out.
        * Used a trained NLP model to extract relationships between pairs of entities out.


### TigerGraph and Zingg

1. **[Entity Resolution with TigerGraph](https://towardsdatascience.com/entity-resolution-with-tigergraph-add-zingg-to-the-mix-95009471ca02):** An article discussing how to use TigerGraph and Zingg for entity resolution.

2. **[Using a Graph Database for Big Data Entity Resolution](https://www.tigergraph.com/blog/using-a-graph-database-for-big-data-entity-resolution/):** A blog post from TigerGraph on using their graph database for big data entity resolution.

3. **[Zingg Github Repository](https://github.com/zinggAI/zingg):** The GitHub repository for Zingg, a tool for entity resolution and matching records.


### PyJedAI:

1. **[PyJedAI CleanCleanER](https://pyjedai.readthedocs.io/en/latest/tutorials/CleanCleanER.html):** A tutorial for using PyJedAI for entity matching and clustering.

2. **[PyJedAI Similarity Joins](https://pyjedai.readthedocs.io/en/latest/tutorials/SimilarityJoins.html):** A tutorial for using PyJedAI for similarity joins in entity resolution.

3. **[ER Evaluation Framework](https://github.com/Valires/er-evaluation?tab=readme-ov-file):** A framework for evaluating entity resolution systems.


### REBEL + Llama Index:

**[REBEL extracts triplets from text](https://medium.com/@sauravjoshi23/building-knowledge-graphs-rebel-llamaindex-and-rebel-llamaindex-8769cf800115):** This is chunked to ensure REBEL can extract the information out.


### KnowledgeGraph

[KnowledgeGraph](https://github.com/rahulnyk/knowledge_graph): This demonstrates a framework from going from document to graph. - the codebase would likely need reworking.

1. **[Use Mistral7B OpenOrca hosted by Ollama](https://huggingface.co/Open-Orca/Mistral-7B-OpenOrca)**: For extracting out triplets.

2. **[NetworkX](https://networkx.org/)** to make graphs.

3. **[PyVis](https://pyvis.readthedocs.io/en/latest/)** to visualise the graphs.

### Graph_Maker: Requires GROQ

1.  Define your own ontology i.e. your entities and a description of what those entities are.

2. Run the Graph-maker using a large language model to create your graph.

3. Then you can use this graph and created it over your documents.

4. [Tutorial](https://towardsdatascience.com/text-to-knowledge-graph-made-easy-with-graph-maker-f3f890c0dbe8)

### Instructor:

1. Might support **[Ollama](https://github.com/jxnl/instructor/blob/main/docs/examples/ollama.md)**
2. You can follow **[this tutorial](https://python.useinstructor.com/examples/knowledge_graph/#generating-knowledge-graphs)** but use the ollama implementation.
