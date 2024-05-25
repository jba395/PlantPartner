import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import src.constants as c
import src.data as data
import src.graph as graph


def planter_algorithm(input_graph: nx.Graph, output_graph: nx.Graph) -> nx.Graph:
    """
    :param input_graph: The graphical representation of the garden elements,
    where each vertex is a plant type and each edge is its friendliness
    to the plant to which it is connected.
    :param output_graph: The result of the optimum garden configuration.
    :return: A graph that indicates the lowest-cost neighbor arrangement for the garden.
    """
    print("\nPLANTING ALGORITHM")
    for i in range(c.NEIGHBOR_LIMITS):

        # Search through all nodes in the graph
        # No difference between input and output nodes
        for node in input_graph.nodes:
            print("Evaluating node " + node)

            # Continue if there are few enough existing connections
            output_node_neighbors = list(output_graph.neighbors(node))
            output_node_degree = len(output_node_neighbors)
            if output_node_degree < c.NEIGHBOR_LIMITS:
                print("Got inside the degree condition")
                min_weight = 99999999
                min_edge = None

                # Search through all edge weights associated with a given node
                for edge in input_graph.edges(node):
                    print("EDGE")
                    print(edge)
                    if input_graph.edges[edge[0], edge[1]]["weight"]:
                        print("Found weight!")


                # for input_neighbor in input_node_neighbors:
                #     print("Evaluating " + input_node + " neighbor " + input_neighbor)
                #     if not output_graph.has_edge(input_node, input_neighbor):
                #         if (input_node, input_neighbor)["Weight"]:
                #             pass

if __name__ == "__main__":
    # Fetch data
    garden_matrix = data.get_garden_matrix()
    print("\nGARDEN MATRIX")
    print(garden_matrix)

    # Get plant names and edges
    plants = data.get_plants(
        matrix=garden_matrix
    )
    print("\nPLANT SET")
    print(plants)

    plant_edges = data.get_plant_edges(
        plants=plants
    )
    print("\nPLANT EDGES")
    print(plant_edges)

    # Get unique blank names and edges
    blanks = data.get_blanks(
        num_plants=len(plants), 
        neighbor_limits=c.NEIGHBOR_LIMITS
    )
    print("\nBLANKS")
    print(blanks)

    blank_edges = data.get_blank_edges(
        plants=plants,
        blanks=blanks,
        neighbor_limits=c.NEIGHBOR_LIMITS
    )
    print("\nBLANK EDGES")
    print(blank_edges)

    print("\nBlanks again")
    print(blanks)

    # exit(0)
    # Concatenate all nodes and edges
    nodes = plants.union(blanks)
    print("\nNODES HERE")
    print(nodes)

    print("\nWhat about plants?")
    print(plants)

    print("\nWhat about manually?")
    print(plants)
    print(blanks)
    print(plants.union(blanks))

    edges = plant_edges.union(blank_edges)

    print("\nNODES HERE")
    print(nodes)

    # Build the input graph
    input_graph = graph.build_graph(
        matrix=garden_matrix,
        nodes=plants.union(blanks),
        edges=plant_edges.union(blank_edges)
    )

    print("\nINPUT NODES")
    print(input_graph.nodes)

    output_graph = graph.build_graph(
        matrix=garden_matrix,
        nodes=plants.union(blanks),
        edges=set()
    )
    print("\nOUTPUT GRAPH NODES")
    print(output_graph.nodes)

    # nx.draw(input_graph, with_labels=True)
    # labels = {e: input_graph.edges[e]['weight'] for e in input_graph.edges}
    # pos = nx.spring_layout(input_graph)  # For better example looking
    # nx.draw_networkx_edge_labels(input_graph, pos)
    # plt.show()


    output_graph = planter_algorithm(
        input_graph=input_graph,
        output_graph=output_graph
    )

    # nx.draw(output_graph, with_labels=True)
    # labels = {e: output_graph.edges[e]['weight'] for e in graph.edges}
    # pos = nx.spring_layout(output_graph)  # For better example looking
    # nx.draw_networkx_edge_labels(output_graph, pos)
    # plt.show()