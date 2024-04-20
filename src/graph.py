import networkx as nx
import src.data as data

def build_graph(nodes, edges):
    G = nx.Graph()

    # Initialize all vertices
    G.add_nodes_from(nodes)

    # Add blank spaces
    blank_counter = 0
    for node in list(G.nodes):
        for i in range(neighbor_limits):
            new_node = c.BLANK_PREFIX + blank_counter
            G.add_node(new_node)
            G.add_edge(node, new_node, weight=c.BLANK_WEIGHT)
            blank_counter += 1

    # Create clique
    for index, row in matrix.iterrows():
        for index2, row2 in matrix.iterrows():
            if index != index2:
                weight = get_weight(
                    matrix_row=row,
                    neighbor=row2[c.PLANT_NAME_COLUMN],
                    friend_weight=1,
                    neutral_weight=2,
                    foe_weight=4
                )
                G.add_edge(row[c.PLANT_NAME_COLUMN], row2[c.PLANT_NAME_COLUMN], weight=weight)

    return G