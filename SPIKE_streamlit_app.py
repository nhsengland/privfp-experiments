from streamlit_annotation_tools import text_labeler
import streamlit as st
import argparse
import json
from src.extraction.extraction import Extraction
from src.config.experimental_config import load_experimental_config
from src.config.global_config import load_global_config

global_config_path = "config/global_config.yaml"
global_config = load_global_config(global_config_path)

default_config_path = "config/experimental_config.yaml"
experimental_config = load_experimental_config(default_config_path)


# Initialize the session state once at the start of the app
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    # Get data using the path passed into streamlit
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", "--data", type=str)

    args = parser.parse_args()
    data_path = args.d

    # Read data
    with open(data_path) as file:
        st.session_state["data"] = json.load(file)

    for i in range(len(st.session_state["data"])):
        st.session_state[i + 1] = {}

data = st.session_state["data"]


def update():
    """
    This updates the streamlit app with the most up to date information.
    """

    # Load the temporary session state
    temp = st.session_state["temp"]
    st.session_state[temp["id"]] = temp["annotations"]

    if isinstance(
        temp["annotations"], dict
    ):  # Check if a dictionary, annotate can return an empty array
        keys = list(temp["annotations"].keys())

        for i in range(len(data)):  # Add keys to all session states
            for key in keys:
                if key not in st.session_state[i + 1].keys():
                    st.session_state[i + 1][key] = []


def annotation_tool(data: dict):
    """Builds the annotation tool with Streamlit.

    Args:
        data (dict): _description_
    """

    # Initialise slider.
    slider_id = st.slider(
        "Select Clinician Note",
        1,
        len(data),
        on_change=update,
        key="my_slider",
    )

    string = data[slider_id - 1]
    labels = st.session_state[slider_id]

    # Pass the string and labels into the annotation tool.
    annotations = text_labeler(string.replace("\n", "  "), labels)

    # Update temporary session state.
    st.session_state["temp"] = {"id": slider_id, "annotations": annotations}

    # Create Named Entity Recognition button.
    NER = st.button("NER :mag:")
    if NER:
        update()  # Update session state with current temp state
        extract()  # Extract,
        update()  # Update session state with new extractions
        st.experimental_rerun()


def extract():
    """Uses NER to extract entites."""

    # Load temporary session state.
    temp = st.session_state["temp"]

    # Check if the annotations are a dictionary.
    if isinstance(temp["annotations"], dict):

        # Extract keys.
        keys = list(temp["annotations"].keys())
        experimental_config.extraction.entity_list = keys

        string = data[temp["id"] - 1]
        # Run extraction.
        results = Extraction(
            global_config=global_config,
            extractionconfig=experimental_config.extraction,
            llm_input=[string.replace("\n", "  ")],
        ).run_or_load(save=False)

        for r in results:
            entities = r["Entities"]
            # Format entity into correct format.
            for entity in entities:

                a = {
                    "start": entity["start"],
                    "end": entity["end"],
                    "label": entity["text"],
                }

                # Add new entities to session state.
                if a not in st.session_state[temp["id"]][entity["label"]]:

                    if entity["label"] in keys:
                        st.session_state[temp["id"]][entity["label"]] += [a]
                    else:
                        st.session_state[temp["id"]][entity["label"]] = [a]

    print("Extraction Done")
    return None


annotation_tool(data)

verbose = False
if verbose:
    st.write(st.session_state)
