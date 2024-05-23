import math
import numpy as np
import plotly.graph_objects as go
import networkx as nx

from typing import List, Tuple, Dict, Any


def draw_dag_graph(config_handler: Any, path_outputs: Dict[str, Any]) -> None:
    """Creates a dag graph showing the experimental workflow

    Args:
        config_handler (_type_): This is the config handler that has been defined.
        path_outputs (_type_): This is the location of the outputs created from the experimental handler.
    """
    relationships = get_relationships(config_handler)
    positions, figsize_height = get_dag_positions(relationships)

    # Create a directed graph
    G = nx.DiGraph()
    G.add_edges_from(relationships)

    # Extract node positions and names
    node_x = []
    node_y = []
    node_text = []
    hover_text = []
    for node, pos in positions.items():
        x, y = pos
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)  # Use the original node name for text labels
        hover_text.append(
            path_outputs.get(node, "")
        )  # Use path_outputs dictionary for hover text

    # Extract edge positions
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)  # None separates the segments
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Create edge trace
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="gray"),
        hoverinfo="none",
        mode="lines",
    )

    # Create node trace
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,  # Use node names for text labels
        textposition="top center",
        hovertext=hover_text,  # Use path_outputs for hover text
        hoverinfo="text",
        marker=dict(showscale=False, color="skyblue", size=10, line_width=2),
    )

    if figsize_height < 600:
        figsize_height = 600

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Experimental Pipeline",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            xaxis=dict(
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
            ),
            yaxis=dict(
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
            ),
            annotations=[
                dict(
                    text="",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            height=figsize_height,  # Adjust the height
            width=800,  # Adjust the width
        ),
    )

    fig.show()


def get_relationships(config_handler: Any) -> List[Tuple]:
    """Function that gets the edges of where there is a connection between nodes.

    Args:
        config_handler (ExperimentalConfigHandler): The defined config handler.

    Returns:
        List[Tuple]: A list of tuples which shows the connections between each nodes.
    """
    relationships = []

    for config in config_handler.load_experimental_config("generate"):
        synthea_path = config.synthea_path.split("/")[-1].split(".")[0]
        path_output = config.path_output.split("/")[-1].split(".")[0]
        relationships.append((synthea_path, path_output))

    for config in config_handler.load_experimental_config("extraction"):
        llm_path = config.llm_path.split("/")[-1].split(".")[0]
        path_output = config.path_output.split("/")[-1].split(".")[0]
        relationships.append((llm_path, path_output))

    return relationships


def get_connections_and_count(relationships: List[Tuple]) -> Any:
    """Creates a dictionary which shows the relationships between the name of each
       component file, and the number of components per component section.

    Args:
        relationships (List[Tuple]): A list of tuples which shows the connections between each nodes.

    Returns:
        connections Dict[str, Any]: This is a nested dictionary of components that map to one another.
        connections_count Dict[str, int]: This is a dictionary where each component has it's number count.
    """

    connections = dict()
    generate_count = 0
    extraction_count = 0
    synthea_paths = list(
        set(
            [
                path1
                for path1, path2 in relationships
                if path1.startswith("synthea")
            ]
        )
    )
    synthea_count = len(synthea_paths)

    for synthea_path in synthea_paths:
        generate_paths = [
            path2 for path1, path2 in relationships if path1 == synthea_path
        ]
        generate_count += len(generate_paths)
        inner_dict = dict()
        for generate_path in generate_paths:
            extraction_paths = [
                path2
                for path1, path2 in relationships
                if path1 == generate_path
            ]
            extraction_count += len(extraction_paths)
            inner_dict[generate_path] = extraction_paths

        connections[synthea_path] = inner_dict

    connections_count = {
        "synthea": synthea_count,
        "generate": generate_count,
        "extraction": extraction_count,
    }

    return connections, connections_count


def get_dag_positions(relationships: List[Tuple]) -> Any:
    """This creates the dag positions so they can sit equidistance apart and make sure
       edges do not crossover.

    Args:
        relationships (List[Tuple]): A list of tuples which shows the connections between each nodes.

    Returns:
        pos (Dict[str, Tuple]): This is a dictionary where the string is the pathname,
                                and the tuple is the coordinate of where the path sits on the DAG diagram.
        figsize_h (int): This is the height that is passed into the DAG code to generate the figure.
    """

    connections, connections_count = get_connections_and_count(relationships)

    extraction_num = (math.ceil(connections_count["extraction"] / 2)) * 2
    pos_list = [i for i in range(0, extraction_num, 2)]
    neg_list = [-1 * i for i in pos_list]
    if connections_count["extraction"] % 2 == 0:
        pos_list.append(connections_count["extraction"])
    extraction_list = pos_list[::-1] + neg_list[1:]
    extraction_tuples = [(2, val) for val in extraction_list]

    pos = dict()

    for synthea_path in connections.keys():
        generate_tuples = []
        for generate_path in connections[synthea_path].keys():
            extraction_paths = connections[synthea_path][generate_path]

            # Extract out the tuples for each extraction class
            sub_extraction_tuples = extraction_tuples[: len(extraction_paths)]
            extraction_tuples = extraction_tuples[len(extraction_paths) :]
            extraction_dict = dict(
                zip(extraction_paths, sub_extraction_tuples)
            )
            pos.update(extraction_dict)

            # Create your generate tuple location
            generate_tuple = (
                1,
                np.mean([val2 for _, val2 in sub_extraction_tuples]),
            )
            generate_tuples.append(generate_tuple)
            pos[generate_path] = generate_tuple

        # Create your synthea tuples
        synthea_tuple = (0, np.mean([val2 for _, val2 in generate_tuples]))
        pos[synthea_path] = synthea_tuple

    figsize_h = connections_count["extraction"] * 80
    return pos, figsize_h
