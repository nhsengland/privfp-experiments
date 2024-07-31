# Annotation SPIKE

This folder has been created to showcase our work researching labelling and annotation tools.

We have researched these tools for the following reasons:
- Users may want to explore a new dataset.
- Users may want to see how effective the NER tool is with different entitiy names.

# Streamlit

To use the streamlit tool, you will need to run the following command in your terminal:

```console
streamlit run SPIKE_streamlit_app.py -- --d "example_output/example_pipeline_17_06_24/llm.json"
```

The string folling the --d argument should be the path to your data.

# ipyWidgets

To use the ipywidgets tool follow the instructions in the widgets_labelling notebook.

You may need to run the notebook in your browser if the ipyWidget fdoes not compile. Run:

```console
jupyter notebook --allow-root
```
