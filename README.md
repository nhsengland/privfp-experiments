# {Privacy FingerPrint}

### About the Project

[![status: experimental](https://github.com/GIScience/badges/raw/master/status/experimental.svg)](https://github.com/GIScience/badges#experimental)

This repository holds code for Privacy Fingerprint. The aim of this project is to develop a modular tool that could be used to calculate a privacy risk score on unstructured clinical data.

[Link to original project propsoal](https://nhsx.github.io/nhsx-internship-projects/)

_**Note:** Only public or fake data are shared in this repository._

## Project structure

```text
+---data                              <- Folder where synthetic data is stored.                    
|
+---docs                              <- Folder to hold further documentation about the project.
|   |      model_card.md              <- A Markdown that provides more information about the code usage.
|
+---models                            <- Folder to hold all saved models to help run pipelines faster after configuration has been run.
|
+---notebooks                         <- Folder containing notebooks to explore each modules' code. 
|   +---generative_module             <- Folder containing notebooks that run the generative module.
|   +---extraction_module             <- Folder containing notebooks that run the extraction module.
|     
|
+---src                               <- Scripts with functions for use in .ipynb notebooks located in the notebooks folder.
|   +---ner_pipeline                  <- Contains scripts that can be used to run a named-entity-recognition pipeline.
|
|   .gitignore                        <- Files (& file types) automatically removed from version control for security purposes
|   config.toml                       <- Configuration file with parameters we want to be able to change (e.g. date)
|   environment.yml                   <- Conda equivalent of requirements file
|   pyproject.toml                    <- Configuration file containing package build information
|   LICENCE                           <- License info for public distribution
|   README.md                         <- Quick start guide / explanation of your project 

### Built With

[![Python v3.8](https://img.shields.io/badge/python-v3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

### Getting Started

#### Installation

Assuming you have set up SSH credentials with this repository the package can be installed from Github directly by running:

`git clone https://github.com/nhsengland/privfp-gen-experiments.git`

To create a suitable environment:
- ```python -m venv _env```
- `source _env/bin/activate`
- `pip install -r requirements.txt`

#### Dependencies

### Usage
{DESCRIPTION OF CODE}

#### Outputs
{LIST AND DESCRIPTION OF OUTPUTS}

{NOTES ON REPRODUCIBILITY OF RESULTS}

#### Datasets
{DESCRIPTION AND LINKS TO DATASETS}

{LINK TO FAKE DATA TO SUPPORT INITAIL CODE RUNS}

### Roadmap

See the {LINK TO REPO ISSUES} for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

_See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidance._

## License

Unless stated otherwise, the codebase is released under [the MIT Licence][mit].
This covers both the codebase and any sample code in the documentation.

_See [LICENSE](./LICENSE) for more information._

The documentation is [© Crown copyright][copyright] and available under the terms
of the [Open Government 3.0][ogl] licence.

[mit]: LICENCE
[copyright]: http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/
[ogl]: http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

## Contact

**This repository is maintained by NHS England Data Science Team**.
To contact us raise an issue on Github or via [email](mailto:datascience@nhs.net)._

## Acknowledgements

- [Scarlett Kynoch](https://github.com/scarlett-k-nhs)
- [Xiyao Zhuang](https://github.com/xiyaozhuang)
- [Dan Schofield](https://github.com/danjscho)