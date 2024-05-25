import pandas as pd
import src.constants as c


def get_garden_matrix() -> pd.DataFrame:
    """
    Fetch the garden matrix.

    :return: A Pandas DataFrame of the garden matrix
    """
    df = pd.read_excel(c.MATRIX_FILENAME)
    df = df.apply(lambda x: x.astype(str).str.upper())
    return df[:2]


def get_plants(matrix: pd.DataFrame) -> set:
    """
    Get a set of the in-scope plant names.

    :param matrix: The dataframe plant matrix
    :return: A set of plant names
    """
    plant_set = set()
    for index, row in matrix.iterrows():
        plant_set.add(row[c.PLANT_NAME_COLUMN])
    return plant_set


def get_blanks(num_plants: int, neighbor_limits: int) -> set:
    """
    Get a set of "blank" node names. They are named arbitrarily yet uniquely.

    :param num_plants: The number of plant types in the garden
    :param neighbor_limits: The maximum number of neighbors for each plant type
    :return: A set of blank node names
    """
    blank_set = set()
    for i in range(num_plants * neighbor_limits):
        blank_set.add(c.BLANK_PREFIX + str(i))
    return blank_set


def get_plant_edges(plants: set) -> set:
    """
    Get a set of edges among plants. The configuration is that of a clique.

    :param plants: A set of plant type names in the garden
    :return: A set of edge specifications comprising a clique in all plant types
    """
    edge_set = set()
    for plant1 in plants:
        for plant2 in plants:
            if plant1 != plant2:
                # This check ensures that we don't see double edges (e.g. A->B & B->A)
                if (plant2, plant1) not in edge_set:
                    edge_set.add((plant1, plant2))
    return edge_set


def get_blank_edges(plants: set, blanks: set, neighbor_limits: int) -> set:
    """
    Get a set of edges among the plants and their blank spots.

    :param plants: A set of plant type names in the garden
    :param blanks: A set of blank names
    :param neighbor_limits: The maximum number of neighbors for each plant type
    :return: A set of edge specifications for each of the plants with their blanks
    """
    edge_set = set()
    blanks_copy = blanks.copy()
    for plant in plants:
        for neighbor in range(neighbor_limits):
            edge_set.add((plant, blanks_copy.pop()))
    return edge_set


def get_relationships(matrix: pd.DataFrame, plant: str, relationship: str) -> set:
    """
    Given the plant data and a particular plant, obtain either the friends
    or foes of that plant.

    :param matrix: The Pandas DataFrame corresponding to the garden
    :param plant: The plant type name
    :param relationship: Either "friend" or "foe"
    :return: All of the friends or foes of the plant type in question
    """
    # Determine relationship to query
    if relationship.upper() == c.FRIEND_VALUE:
        col = c.FRIEND_COLUMN
    elif relationship.upper() == c.FOE_VALUE:
        col = c.FOE_COLUMN

    # Parse the plants in that relation type
    row = matrix.loc[matrix[c.PLANT_NAME_COLUMN] == plant]
    relation_data = row.iloc[0][c.FRIEND_COLUMN]
    relation_data = relation_data.split(",")
    
    # Create a set with trimmed whitespace for each element
    relations = set()
    for relation in relation_data:
        relations.add(relation.upper().strip())
    return relations


def get_plant_relationship(matrix: pd.DataFrame, plant_1: str, plant_2: str) -> str:
    """
    Given two plants, determine their relationship to one another.

    :param matrix: The Pandas DataFrame corresponding to the garden
    :param plant_1: The plant type whose relationships we are seeking
    :param plant_2: The plant type being searched among plant_1's relationships
    :return: A string corresponding to 
    """
    # Get set of friends
    friends = get_relationships(
        matrix=matrix,
        plant=plant_1,
        relationship=c.FRIEND_VALUE
    )

    if plant_2 in friends:
        return c.FRIEND_VALUE

    # Get set of foes
    foes = get_relationships(
        matrix=matrix,
        plant=plant_1,
        relationship=c.FOE_VALUE
    )

    if plant_2 in foes:
        return c.FOE_VALUE

    return c.NEUTRAL_VALUE
