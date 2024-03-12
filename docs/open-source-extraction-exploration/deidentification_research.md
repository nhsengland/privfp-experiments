# De-Identification Methods

Deidentification techniques refer to methods used to remove or mask personally identifiable information (PII) from data, while still retaining its utility for analysis or other purposes. 

!!! info "De-Identification Methods"

    === "Presido"

        [Presido](https://microsoft.github.io/presidio/) is a de-identification SDK owned by microsoft.
       
        * Regex to recognise patterns.
        * Use Named-entity recognition model (default is set to **en_core_web_lg** and supports any Spacy model.)
        * Validating patterns
        * Uses context to increase detection confidence.

    === "AnonCAT"
        [AnonCAT](https://cogstack.org/anoncat-de-identification-nlp-with-cogstack-medcat/) is a transformer based approach fo redacting text from electronic health records.

        It uses a NER model, **en_core_sci_md**, to detect all medical terms. Then they assign each entitity to an ID in a biomedical databases (UMLS) to normalise the outputs. (decipher new diagnosis, history, or reason for admission.)

    === "MASK"

        [MASK](https://github.com/icescentral/MASK_public) is Manchester University de-identification framework for named-entitity-recognition.

        * BiLSTM layer - essentially considers each of the entities (beginning, in the middle, no entity) - and assigns a confidence value to help determine it's label across.
        * CRFs Layer use the observed data to predict the labels of the sequence, while taking into account the dependencies between neighbouring labels. (Conditional Random Field)
        * GLoVe embeddings - determines a word vector space that incorporates both the local context of words but also their co-occurence with other words across the space. 
        * ELMo embeddings - considers where words have the same spelling but different meaning (Polysemy.)  - takes the word representations and then take the entire input sentence into equation for calculating the word embeddings.

    === "Cloud Data Loss Prevention API"

        [DLP API](https://cloud.google.com/dlp/docs/reference/rest) is googles API for detection of privacy-sensitive fragments in text, images, and Google Cloud Platform storage repositories.

        There is a range of techniques that are implemented in this [API](https://cloud.google.com/dlp/docs/samples/dlp-inspect-string-multiple-rules), some noticeable ones being:

        * Using basic RegexMatching for some PID data. etc. phone numbers.
        * Using a hotword rule to instruct Sensitive Data Protection to adjust the likelihood of a finding, depending on whether a hotword occurs near that finding.
        * Using exclusion rules to exclude false or unwanted finding (identifying custom substrings within a string.) - for example name inside an email.(Take the email, and not the name)
