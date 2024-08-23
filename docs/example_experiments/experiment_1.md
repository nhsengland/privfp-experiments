# Experiment 1

Let's run an experiment with the Privacy Fingerprint pipeline to understand each section of the pipeline, and explore some of the exploration and experiments we can do within each section. 

The majority of the experimentation done in this example was done following the structure in `notebooks/full_pipeline_example.ipynb`.

## Generating synthetic Patient Data with Synthea

First, we used step one of the `full_pipeline_example.ipynb` notebook to generate 1000 synthetic patient records. We specify 1000 by overriding the experimental config with the following line of code:

```console
experimental_config.synthea.population_num = "1000"
```

Interestingly, this returns to us a list of outputs with a length of 954. Currently, our pipeline filters out duplicate patients and wellness encounters, so this is expected. We can use the fact that this data is structured to still check that each record is unique by running the following python code:

```python
NHS_number_set = set([N["NHS_NUMBER"] for N in output_synthea])
print(len(NHS_number_set))
```

This returns 954. 

## Using a LLM to Generate Synthetic Nedical Notes

We will use LLama 3 to turn each synthea output into a synthetic medical note. As of August 2024, this is not the most up-to-date LLama model. Llama 3.1 is available for download and our pipeline allows for this to be easily changed if you would like. 

Inspecting the outputs we notice a lot of notes start with: "Here is a clinical note..." or "Clinical Note:". Clearly, our prompt needs some fine-tuning if we want our notes to be more realistic. this is again easy to change within our pipeline. 

There is massive variation in the structure of the free text data. If we only take NHS numbers as an example, we see them in multiple different forms. for example:

- 9274572891
- 19632-85395
- 34732-45-801
- 32 64 12 45 56

As a reminder, these NHS numbers are synthetic. Incredibly, these 4 different structures come from the first 4 LLM outputs. In further examples we see full stops, dashes and commas seperating parts of the NHS number. This makes it impossible to use simple techniques like regular expressions to extract all NHS numbers, and so we must rely on more advanced methods of entity extraction. 

## Re-extracting Entities from the Patient Medical Notes

We run extraction using Gliner as our Named Entity Extraction Model. Again, focussing on just NHs Numbers, we find that a total of 1006 NHS Numbers are extracted from our 954  reviews, with only 104 being within the original NHS Number set we previously defined. 

This means that multiple NHS numbers are extracted from some notes. We find that 308 reviews contain more than two NHS number entities extracted. We find that this is always the number representing the NHS number, alongside the text "NHS Number". This leaves us with a new conclusion, lots of NHS number are not being extracted from reviews. 

We find that 256 reviews do not have an NHS number extracted. Given that the NHS numbers are so diverse in structure, it is hard to know whether they are missed due to strange structure, or they are not generated at all.

Looking at the first 10 occasions where no NHS number was extracted, there is never an NHS number generated. The medical note only contains the patient name and date of birth.  

## Normalising Entities Extracted for Scoring

The next step of the pipeline essentially turns our extraction data from a json format to tabular data. It does this using one hot encoding, where each row in the tabular data refers to a medical note id. If two notes contained the same medical number, they would have the same value in the "nhs number" one-hot encoded column. 

Currently, the first instance of an entity in the medical note is the one used for one hot encoding. This has some issues. For example, we know that "NHS Number:" is often extracted as the "nhs number" entity. As this will often appear before the NHS number in medical notes, it is used instead of the true NHS number when we one-hot-encode the data. This issue is something we are aware of, and we have done various research on other methods of standardisation.

One simple fix would be to ensure the NHS Number entitity contains numbers, or does not contain the string "NHS Number".

## Uniqueness of Standardised Entity Values

Once we have tabular data, we can start exploring the privacy risk of our data. We do this by estimating the uniqueness of each data point. The more unique the data, the more identifiable the individual is likely to be. 

The uniqueness is measured using PycorrectMatch, and documentation on how this works can be found at `docs/corect-match/`. To simplify, a score close to 1 means the row is incredibly unique, whilst a score close to 0 is not unique. Currently, the lowest score for any row is 0.998. Therefore, every row is highly reidentifiiable. 

This makes sense, we have not done any anonymisation steps. 

Let us imagine a theoretical anonymisation technique that finds every single NHS number in free text data and replaces it with a blank value. This would mean that in our one hot encoded dataframe, all values in the NHS number column would be one fo two numbers - 0 and 1. 0 would refer to an anonymised NHS number and 1 would refer to no NHS number being present. 

We can alter our transformed dataset using the following line of code:

```python
anonymised_dataset_1["nhs number"] = [random.randint(0,1) for i in range(len(anonymised_dataset_1))]
```

Let's take this further and make an even more anonymised dataset where all names are replaced with the initial of their first, and thus the `person` column only contains 26 values.

```python
anonymised_dataset_1["person"] = [random.randint(0,25) for i in range(len(anonymised_dataset_1))]
```

For the `date of birth` column let's say that the data in anonymised by removing the day, and only keeping the month and the year. Assuming all patients are between 1 and 80, this would leave 960 possible months of birth, however we would expect lots of duplicates. We run the below code to generate a random list with duplicates:

```python
list = []
current_int = 0

for i in range(len(anonymised_dataset_1)):
    list.append(current_int)
    if random.randint(0,1):
        current_int+=1

random.shuffle(list)
```

