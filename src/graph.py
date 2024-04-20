import networkx as nx
import pandas as pd
import src.constants as c
import src.data as data


def get_relationship_weight(matrix: pd.DataFrame, plant_1: str, plant_2: str) -> int:
    """
    Determine the weight associated with two plants' relationship.

    :param matrix: The Pandas DataFrame corresponding to the garden
    :param plant_1: A plant type name (or blank)
    :param plant_2: A plant type name (or blank)
    :return: The edge weight associated with the connection between plant_1 and plant_2
    """
    if c.BLANK_PREFIX in plant_1 or c.BLANK_PREFIX in plant_2:
        return c.BLANK_WEIGHT

    relationship = data.get_plant_relationship(
        matrix=matrix,
        plant_1=plant_1,
        plant_2=plant_2
    )

    if relationship == c.FRIEND_VALUE:
        return c.FRIEND_WEIGHT
    elif relationship == c.FOE_VALUE:
        return c.FOE_WEIGHT
    else:
        return c.NEUTRAL_WEIGHT


def build_graph(matrix: pd.DataFrame, nodes: set, edges: set) -> nx.Graph:
    """
    Generate the input graph for the Planter Algorithm.

    :param nodes: The nodes of the input graph
    :param edges: The edges of the input graph
    :return: A graph G = (V, E) for the input for the Planter Algorithm
    """
    G = nx.Graph()

    # Initialize all vertices
    G.add_nodes_from(nodes)

    # Initialize all edges
    G.add_edges_from(edges)

    # Add edge weights
    for edge in list(G.edges):
        relationship_weight = data.get_relationship_weight(
            matrix=matrix,
            plant_1=edge[0],
            plant_2=edge[1]
        )
        G.edges[edge[0], edge[1]]["weight"] = relationship_weight

    return G
