import matplotlib.pyplot as plt
import networkx as nx
import os
import pandas as pd
import src.constants as c
import src.data as data
import src.graph as graph


def planter_algorithm(input_graph: nx.Graph, output_graph: nx.Graph, plants: set, log) -> nx.Graph:
    """
    :param input_graph: The graphical representation of the garden elements,
    where each vertex is a plant type and each edge is its friendliness
    to the plant to which it is connected.
    :param output_graph: The result of the optimum garden configuration.
    :return: A graph that indicates the lowest-cost neighbor arrangement for the garden.
    """
    print("\nPLANTING ALGORITHM")
    log.write("\n\n\nPLANTING ALGORITHM")
    for i in range(c.NEIGHBOR_LIMITS):
        log.write(f"\n\n\tNeighbor iteration {i}")

        # Search through all nodes in the graph
        # No difference between input and output nodes
        for node in input_graph.nodes:
            if node not in plants:
                log.write(f"\n\t\t{node} is not in the plants set; skipping")
                continue
            print("Evaluating node " + node)
            log.write(f"\n\t\tChecking node {node}")

            # Continue if there are few enough existing connections
            output_node_neighbors = list(output_graph.neighbors(node))
            output_node_degree = len(output_node_neighbors)
            log.write(f"\n\t\t{node} has {output_node_degree} neighbors")

            if output_node_degree < c.NEIGHBOR_LIMITS:
                log.write(f"\n\t\t\t{node} can accept another neighbor")
                log.write(f"\n\t\t\tResetting min weight")
                min_weight = 99999999
                min_edge = None

                # Search through all edge weights associated with a given node
                for edge in input_graph.edges(node):

                    # Check to see if destination node can accept another neighbor
                    neighbor_degree = len(list(output_graph.neighbors(edge[1])))
                    if neighbor_degree >= c.NEIGHBOR_LIMITS:
                        log.write(f"\n\t\t\t\tSkipping {edge[1]} because it cannot accept another neighbor (degree: {neighbor_degree})")
                        continue

                    weight = input_graph.edges[edge[0], edge[1]]["weight"]
                    log.write(f"\n\t\t\t\tMin weight so far: {min_weight}")
                    log.write(f"\n\t\t\t\t{node} edge {edge} is being evaluated with weight {weight}")
                    if weight < min_weight:
                        min_weight = weight
                        min_edge = edge
                        log.write(f"\n\t\t\t\t\tNew min weight found: {min_weight}")
                
                print(f"\n\t\t\tMin edge determined for {node}: {min_edge}" + str(min_edge))
                input_graph.remove_edge(edge[0], edge[1])
                output_graph.add_edge(edge[0], edge[1])
                output_graph.edges[edge[0], edge[1]]["weight"] = min_weight
                log.write(f"\n\t\t\t*****Min edge {min_edge} chosen with weight {min_weight}*****")
            
            else:
                log.write(f"\n\t\t\t{node} CANNOT accept another neighbor")


    return output_graph

if __name__ == "__main__":
    # Set up log file
    os.remove("src/log.txt")
    open("src/log.txt", "a").close()
    log = open("src/log.txt", "a")

    log.write("Starting program")

    # Fetch data
    garden_matrix = data.get_garden_matrix()
    log.write("\nObtained garden matrix\n")

    # Get plant names and edges
    plants = data.get_plants(
        matrix=garden_matrix
    )
    log.write("\n\nPlants in-scope: \n" + str(plants))

    plant_edges = data.get_plant_edges(
        plants=plants
    )
    log.write("\n\nPlant edges in-scope: \n" + str(plant_edges))

    # Get unique blank names and edges
    blanks = data.get_blanks(
        num_plants=len(plants), 
        neighbor_limits=c.NEIGHBOR_LIMITS
    )
    log.write("\n\nBlanks in-scope: \n" + str(blanks))

    blank_edges = data.get_blank_edges(
        plants=plants,
        blanks=blanks,
        neighbor_limits=c.NEIGHBOR_LIMITS
    )
    log.write("\n\nBlank edges in-scope: \n" + str(blank_edges))

    # Concatenate all nodes and edges
    nodes = plants.union(blanks)
    edges = plant_edges.union(blank_edges)

    # Build the input graph
    input_graph = graph.build_graph(
        matrix=garden_matrix,
        nodes=nodes,
        edges=plant_edges.union(blank_edges)
    )
    log.write("\n\nInput nodes: \n" + str(input_graph.nodes))

    print("\nINPUT NODES")
    print(input_graph.nodes)

    output_graph = graph.build_graph(
        matrix=garden_matrix,
        nodes=nodes,
        edges=set()
    )
    log.write("\n\nOutput nodes: " + str(output_graph.nodes))
    
    print("\nOUTPUT GRAPH NODES")
    print(output_graph.nodes)

    nx.draw(input_graph, with_labels=True)
    labels = {e: input_graph.edges[e]['weight'] for e in input_graph.edges}
    pos = nx.spring_layout(input_graph)  # For better example looking
    nx.draw_networkx_edge_labels(input_graph, pos)
    plt.show()

    output_graph = planter_algorithm(
        input_graph=input_graph,
        output_graph=output_graph,
        plants=plants,
        log=log
    )

    # Close the logging file
    log.close()

    nx.draw(output_graph, with_labels=True)
    labels = {e: output_graph.edges[e[0], e[1]]['weight'] for e in output_graph.edges}
    pos = nx.spring_layout(output_graph)  # For better example looking
    nx.draw_networkx_edge_labels(output_graph, pos)
    plt.show()
