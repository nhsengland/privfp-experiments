# PyCanon and Privacy Metrics

[PyCanon](https://github.com/IFCA-Advanced-Computing/pycanon) is a python library which asses the values of common privacy measuring metrics, such as k-Anonymity, i-Diversity and t-Closeness. This page will explain the metrics used in PyCanon, alongside other metrics we have researched and considered.

## PyCanon Metrics

To understand the definitions below, we must first understand identifiers, quasi-identifiers and sensitive attributes. There are defined in the PyCanon [paper](https://www.nature.com/articles/s41597-022-01894-2).

**Identifier:** This is any piece of information, such as a full name or NHS number, which can directly identify an individual.

**Quasi-Identifier** This is a piece of information that when combined with other Quasi-Identifiers can make identification possible. This could include birthdays and education information.

**Sensitive Attributes:** Sensitive attributes contain private information that must not be extracted.

### k-Anonymity

As defined in the PyCanon [paper](https://www.nature.com/articles/s41597-022-01894-2), a database verifies k-anonymity if for each row of the database, there are at least `k-1` indistinguishable rows with respect to the quasi-identifiers. The value of `k` deemed acceptable has to be decided beforehand. The probability of identifying an individual in the database using the quasi-identifiers will be at most `1/k`.

### (α,k)-Anonymity

Given only one sensitive attribute `S`, it is checked if the database is k-anonymous and the frequency of each possible value of `S` is lower or equal than α in each equivalence class.

### l-Diversity

k-anonymity gets you equivalence classes - sets of records in the dataset which share the same values for their quasi identifiers. l-diversity is an extension of this. In the case of one sensitive attribute, it checks whether there are at least `l` distinct values for `S`. `l` must always be greater than or equal to 1.

### Entropy l-Diversity

A database verifies this condition if the entropy of each equivalence class is greater than `log(l)`. The entropy is defined as:

$$
H(EC) = - \sum_{s \in D} p(EC,S) \log_2(p(EC,S))
$$

where `H` is the entropy, `EC` is the equivalence class, `D` is the domain of `S`, where `S` is a sensitive attribute, and `p((EC,S))` is the fraction of of records in the equivalence class that have `S` as a sensitive attribute.

### Recursive (c,l)-Diversity

If a sensitive value is removed from an equivalence class that verifies (c,l) diversity, then (c,l-1) diversity is preserved. PyCanon uses the technique defined in this [paper](https://ieeexplore.ieee.org/document/1617392). If there are `n` different values of of a sensitive attribute in an equivalence class, (c,l)-diversity is verified by looking at the the number of times the i-th most frequent values appear in the equivalence class.

For a more detailed explanation see the official [paper](https://www.nature.com/articles/s41597-022-01894-2).

### Basic β-Likeness and Enhanced β-Likeness

These two techniques can be used in order to control the distance between the distribution of a sensitive attribute in an equivalence class and in the entire database. They follow the method implimented in this [paper](https://arxiv.org/abs/1208.0220).

### t-Closeness

A database with one sensitive attribute `S` verifies t-closeness if all the equivalence classes verify it. An equivalence class verifies t-closeness if the distribution of the values of `S` are at a distance no closer than `t` from the distribution of the sensitive attribute in the whole database.

In PyCanon, [Earth Mover's distance](https://ieeexplore.ieee.org/document/4221659) is used. See this paper and the PyCanon [paper](https://www.nature.com/articles/s41597-022-01894-2) for more information.

### δ-Disclosure Privacy

For a dataset with only one sensitive attribute `S`, the δ-disclosure privacy is verified if:

$$
\log\left(\frac{p(EC,S)}{p(D,S)}\right) < \delta_s,
$$

for every sensitive attribute in the dataset, and every equivalence class. `p(EC,S)` is the fraction of records with `S` as a sensitive attribute in the equivalence class `EC`, and `D` is the dataset.

## Other Metrics

There are various other methods for measuring privacy which are not included in the PyCanon tool. They are well explained in these [blogs](https://desfontain.es/blog/). We will discuss [K-Map](https://desfontain.es/blog/k-map.html) alongside [δ-presence](https://desfontain.es/blog/delta-presence.html). 

### k-Map

Like k-Anonymity, k-Map requires a list of quasi-identifiers. It also requires a larger re-identification dataset. This could be an original dataset before anonymisation, or another larger dataset of everyone living in the UK, for example a census. Your data satisfies k-map if every combination of values for the quasi identifiers appears at least `k` times in the re-identification dataset. Calculating k-Map is very computationally expensive.

### δ-Presence

Similar to k-map, δ-presence is a metric that quantifies the probability that an individual belongs to an anonymised dataset. It is also very computationally expensive.


### Visualisations

Google Cloud's [Looker Studio](https://cloud.google.com/sensitive-data-protection/docs/visualizing_re-id_risk) has a visualisation suite for privacy metrics.

## Anomoly Detection

Our current privacy scoring method uses Named-Entity-Recognition (NER) to extract identifiers and quasi-identifiers, then [PyCorrectMatch](https://github.com/computationalprivacy/pycorrectmatch) measures the data uniqueness of each piece of text based on the extracted entities. Each row is given a score on how unique the data is. Unique pieces of data are assumed to have a higher risk of re-identification.

Following this idea, we instead can explore the use of anomoly detection to identify high risk columns.

### Distance Based Methods

Distance metrics can be used to find outliers. The greater the distance away from other individuals, the more unique they are. Possible [distance metrics](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html) that can be used are:

- Euclidean Distance
- Manhatten Distance
- Minowski Distance

Different distance metrics will have an effect on which data points are considered outliers. As our data is unlikely to be high-dimensional, simple methods such as Euclidean Distance can be both effective and explainable. However, for higher dimensional multi-variate data, more advanced distance metrics could be used, such as Mahalanobis which is effective for high dimensional multi-variate data. 

### Novelty and Outlier Detection

[SKLearn](https://scikit-learn.org/stable/modules/outlier_detection.html) gives examples of models used for anomoly detection, alongside the following definitions for Novelty and Outlier Detection:

**outlier detection:**
The training data contains outliers which are defined as observations that are far from the others. Outlier detection estimators thus try to fit the regions where the training data is the most concentrated, ignoring the deviant observations.

**novelty detection:**
The training data is not polluted by outliers and we are interested in detecting whether a new observation is an outlier. In this context an outlier is also called a novelty.

We are more interested in outlier detection. However, many of these methods need the seperation of training and testing data to be effective, of which many users of the Privacy Fingerprint pipeline will not have. Some options we can use are:

- The [IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html#sklearn.ensemble.IsolationForest) 'isolates' observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature. The `fit_predict` function in SKLearn allows for predictions to be returned on the training data.
- The [Elliptic Envelope](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.EllipticEnvelope.html#sklearn.covariance.EllipticEnvelope) is an object for detecting outliers in a Gaussian distributed dataset. It also has a `fit_predict` function in SKLearn which allows for predictions to be returned on the training data.

### LLM as a (Privacy) Judge

LLM as a judge is a method in which LLM's are used to evaluate the outputs. Following the structure of the prompt in this [huggingface example](https://huggingface.co/learn/cookbook/en/llm_judge#using-llm-as-a-judge--for-an-automated-and-versatile-evaluation), we can design a prompt which asses the privacy risk of each string. Issues with this approach include:

- A model may predict different scores for the same review if prompted on multiple occasions. This could be mitigated by setting the temperature to 0.
- It is very computationally expensive.

### Conclusions

Traditional privacy metrics, such as k-anonymity and l-diversity are well established. K-anonymity was released in [2002](https://www.worldscientific.com/doi/abs/10.1142/S0218488502001648) and thus has been used in various [reports](https://link.springer.com/chapter/10.1007/978-3-642-01718-6_4). As these metrics are so commonly used in privacy studies, it makes sense to implement k-anonymity, l-diversity and t-closeness into our pipeline. 

Given we use [Synthea](https://synthetichealth.github.io/synthea/) to generate our synthetic medical notes dataset, we have a a large re-identification dataset we can use for techniques such as k-map. This may also be worth implementing into our pipeline.

Determining a row-by-row privacy risk score like those found by [PycorrectMatch](../correct-match/what-is-correct-match.md) can be done using distance-based metrics and outlier detection methods. Currently, we have no plan to implement these into our pipelines. 