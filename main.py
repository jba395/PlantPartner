import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import src.constants as c
import src.data as data
import src.graph as graph


def planter_algorithm(graph: nx.Graph):
    """
    :param graph: The graphical representation of the garden elements,
    where each vertex is a plant type and each edge is its friendliness
    to the plant to which it is connected.
    :return: A graph that indicates the lowest-cost neighbor arrangement for the garden.
    """
    pass

if __name__ == "__main__":
    # Fetch data
    garden_matrix = data.get_garden_matrix()
    print(garden_matrix)

    # Get plant names and edges
    plants = data.get_plants(
        matrix=garden_matrix
    )
    print(plants)

    plant_edges = data.get_plant_edges(
        plants=plants
    )
    print(plant_edges)

    # Get unique blank names and edges
    blanks = data.get_blanks(
        num_plants=len(plants), 
        neighbor_limits=c.NEIGHBOR_LIMITS
    )
    print(blanks)

    blank_edges = data.get_blank_edges(
        plants=plants,
        blanks=blanks,
        neighbor_limits=c.NEIGHBOR_LIMITS
    )
    print(blank_edges)

    # Concatenate all nodes and edges
    nodes = plants.union(blanks)
    edges = plant_edges.union(blank_edges)

    # Build the input graph
    input_graph = graph.build_graph(
        matrix=garden_matrix,
        nodes=nodes,
        edges=edges
    )

    nx.draw(output_graph, with_labels=True)
    labels = {e: output_graph.edges[e]['weight'] for e in graph.edges}
    pos = nx.spring_layout(output_graph)  # For better example looking
    nx.draw_networkx_edge_labels(output_graph, pos)
    plt.show()

    output_graph = planter_algorithm(
        graph=input_graph
    )

    # nx.draw(output_graph, with_labels=True)
    # labels = {e: output_graph.edges[e]['weight'] for e in graph.edges}
    # pos = nx.spring_layout(output_graph)  # For better example looking
    # nx.draw_networkx_edge_labels(output_graph, pos)
    # plt.show()