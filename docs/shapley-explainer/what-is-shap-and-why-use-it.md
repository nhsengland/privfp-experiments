# What is Shapley and Why use it?

## What is Shapley?

SHAP is proposed as a unified measure of feature importance of a machine learning model by assigning each feature an importance value for each prediction.

The sum of SHAP values for all features is equal to an individual prediction minus the prediction for some baseline values. The graph below illustrates an example for whether a team would have a player win the Man of the Match award in a game of football.

![Shapley: Explainer Graph](assets/images/shapley_explainer_graph.png)

SHAP is an open source Python library which implements the methods described in the original paper.

* **SHAP**: https://github.com/shap/shap
* A Unified Approach to Interpreting Model Predictions: https://papers.nips.cc/paper_files/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html
* More citations: https://github.com/shap/shap?tab=readme-ov-file#citations

## Why use Shapley?

It is important to be able to interpret the results of machine learning models and by understanding feature contributions to individual predictions, we can gain insight into how models arrive at specific outcomes. This is crucial for building trust in complex models that are often difficult to interpret.