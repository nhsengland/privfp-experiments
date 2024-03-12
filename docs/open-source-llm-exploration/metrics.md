# Metrics to assess the quality of generated outputs

This section discusses particular quantitative metrics we could use. It would be useful to evaluate on domain specific tasks as well as general LLM tasks.

## Topics

- Coherence: Does the output make sense?
- Relevance: Is the output relevant to the prompt?
- Fluency: Is the output grammatically correct?
- Context understanding: Is the output style correct?
- Diversity: How much does the output style vary?

## Metrics

[HF Evaluate Metric](https://huggingface.co/evaluate-metric)
    
Provides a wide range of evaluation metrics out of the box. Here are three examples:

- [Perplexity](https://huggingface.co/spaces/evaluate-metric/perplexity)
    - [Documentation](https://huggingface.co/docs/transformers/perplexity)
    - Perplexity is a measurement of how well a probability distribution or probability model predicts a sample
    - Intuitively, perplexity can be understood as a measure of uncertainty. The perplexity of a language model can be seen as the level of perplexity when predicting the next word in a sequence. Good read: [Understanding evaluation metrics for language models](https://thegradient.pub/understanding-evaluation-metrics-for-language-models/)
    - Practically, calculation of perplexity will depend on the context length of the LLM and HF Transformers provides an example on how to do this using a "sliding window" approach.

- [BLEU](https://huggingface.co/spaces/evaluate-metric/bleu)
    - Bilingual Evaluation Understudy is a metric calculated by comparing machine/human natural language translations
    - Requires human translation reference

- [ROUGE](ttps://huggingface.co/spaces/evaluate-metric/rouge)
    - Recall-Oriented Understudy for Gisting Evaluation is a metric calculated by comparing machine/human summarisations
    - Requires human summarisation reference

## Further reading

- [A Metrics-First Approach to LLM Evaluation](https://www.rungalileo.io/blog/metrics-first-approach-to-llm-evaluation)

- [Semantic Uncertainty](https://arxiv.org/abs/2302.09664)

    Introduce semantic entropy, a metric which incorporates linguistic invariances created by shared meanings to provide a more - predictive metric of model accuracy.

- [FEVER](https://arxiv.org/abs/1803.05355)

    Introduces Fact Extraction and VERification, a publicly available dataset for verification against textual sources

- [ProoFVer](https://arxiv.org/abs/2108.11357)

    Proposes fact verification system which uses a seq2seq model to generate natural logic-based inferences as proofs.

## Challenges

- Subjective human evaluation
- Over-reliance on perplexity
- Difficult to capture diversity and creativity
- Metric performance won't necessarily translate to real use case performance
- Dataset bias