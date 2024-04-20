import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def get_garden_matrix():
    df = pd.read_excel("garden_matrix.xlsx")
    return df[:4]


def build_graph(matrix, neighbor_limits: int, blank_threshold: int):
    G = nx.Graph()
    plants = []

    # Initialize all vertices
    for index, row in matrix.iterrows():
        plants.append(row["Plant"])
    G.add_nodes_from(plants)

    # Add blank spaces
    blank_counter = 0
    for node in list(G.nodes):
        for i in range(neighbor_limits):
            G.add_node("Blank_{}".format(blank_counter))
            G.add_edge(node, "Blank_{}".format(blank_counter), weight=blank_threshold)
            blank_counter += 1

    # Create clique
    for index, row in matrix.iterrows():
        for index2, row2 in matrix.iterrows():
            if index != index2:
                weight = get_weight(
                    matrix_row=row,
                    neighbor=row2["Plant"],
                    friend_weight=1,
                    neutral_weight=2,
                    foe_weight=4
                )
                G.add_edge(row["Plant"], row2["Plant"], weight=weight)

    return G

def get_weight(matrix_row, neighbor, friend_weight, neutral_weight, foe_weight):
    neighbor = neighbor.upper()
    friends = matrix_row["Friend"].split(",")
    friends_formatted = []
    for friend in friends:
        friends_formatted.append(friend.upper().strip())

    foes = matrix_row["Foe"].split(",")
    foes_formatted = []
    for foe in foes:
        foes_formatted.append(foe.upper().strip())

    print(friends_formatted)
    print(foes_formatted)
    print(neighbor)

    if neighbor in friends_formatted:
        print(f"{neighbor} is a friend of {matrix_row['Plant']}")
        return friend_weight
    
    elif neighbor in foes_formatted:
        print(f"{neighbor} is a foe of {matrix_row['Plant']}")
        return foe_weight
    
    else:
        print(f"{neighbor} is neither friend nor foe of {matrix_row['Plant']}")
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
    garden_matrix = get_garden_matrix()
    graph = build_graph(garden_matrix, 2, 3)

    nx.draw(graph, with_labels=True)
    labels = {e: graph.edges[e]['weight'] for e in graph.edges}
    pos = nx.spring_layout(graph)  # For better example looking
    nx.draw_networkx_edge_labels(graph, pos)
    plt.show()