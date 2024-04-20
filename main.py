import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import src.constants as c
import src.data as data
import src.graph as graph

def get_weight(matrix_row, neighbor, friend_weight, neutral_weight, foe_weight):
    neighbor = neighbor.upper()
    friends = matrix_row[c.FRIEND_COLUMN].split(",")
    friends_formatted = []
    for friend in friends:
        friends_formatted.append(friend.upper().strip())

    foes = str(matrix_row["Foe"]).split(",")
    foes_formatted = []
    for foe in foes:
        foes_formatted.append(foe.upper().strip())

    # print("Friends: " + str(friends_formatted))
    # print("Foes: " + str(foes_formatted))
    # print("Neighbor being evaluated: " + neighbor)
    # print("\n")

    if neighbor in friends_formatted:
        # print(f"{neighbor} is a friend of {matrix_row['Plant']}")
        return friend_weight
    
    elif neighbor in foes_formatted:
        # print(f"{neighbor} is a foe of {matrix_row['Plant']}")
        return foe_weight
    
    else:
        # print(f"{neighbor} is neither friend nor foe of {matrix_row['Plant']}")
        return neutral_weight


def main(graph, neighbor_limits: int):
    """
    :param graph: The graphical representation of the garden elements,
        where each vertex is a plant type and each edge is its friendliness
        to the plant to which it is connected.
    :param neighbor_limits: The maximum number of neighbors that any given
        plant may have.
    :return: A graph that indicates the lowest-cost neighbor arrangement for the garden.
    """
    pass

if __name__ == "__main__":
    # Fetch data
    garden_matrix = get_garden_matrix()

    # Get plant names and edges
    plants = data.get_plants(
        matrix=garden_matrix
    )

    plant_edges = data.get_plant_edges(
        plants=plants
    )

    # Get unique blank names and edges
    blanks = data.get_blanks(
        num_plants=len(plants), 
        neighbor_limits=c.NEIGHBOR_LIMITS
    )

    blank_edges = data.get_blank_edges(
        plants=plants,
        blanks=blanks,
        neighbor_limits=c.NEIGHBOR_LIMITS
    )

    # Build a graph
    graph = build_graph(garden_matrix, 2, 3)

    nx.draw(graph, with_labels=True)
    labels = {e: graph.edges[e]['weight'] for e in graph.edges}
    pos = nx.spring_layout(graph)  # For better example looking
    nx.draw_networkx_edge_labels(graph, pos)
    plt.show()