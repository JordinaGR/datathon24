import numpy as np
import pandas as pd
from pyvis.network import Network
import networkx as nx
from k_means_constrained import KMeansConstrained
from matplotlib import cm

from participant import load_participants

data_path = "data/datathon_participants.json"
participants = load_participants(data_path)


participants = participants[200:225]
n = len(participants)
print("Num. participants:", n)

N_COLORS = 100

# diccionaris de mappeig
YEAR_TO_NUM = {
    '1st year': 1,
    '2nd year': 2,
    '3rd year': 3,
    '4th year': 4,
    'Masters': 5,
    'PhD': 6
}


COLOR_MAP_EDGES = cm.get_cmap("RdYlGn")
COLOR_MAP_NODES = cm.get_cmap("hsv")


def cluster_to_color(cluster_id: int, n_clusters: int) -> str:
    r, g, b, a = COLOR_MAP_NODES(cluster_id/n_clusters)
    return f"rgb({round(255*r)},{round(255*g)},{round(255*b)})"

def percentage_to_color(f: float) -> str:
    r, g, b, a = COLOR_MAP_EDGES(f)
    return f"rgb({round(255*r)},{round(255*g)},{round(255*b)})"


def make_graph(
    preferred_role_mult: float,
    interests_mult: float,
    year_mult: float,
    friend_mult: float,
    challenges_mult: float,
    languages_mult: float,
    edge_max_width: int,
    edge_threshold: float,
    n_clusters: int
) -> nx.Graph:

    nodes = pd.DataFrame(data=[[p.id, p.name] for p in participants], 
                         columns=['id', 'label'])

    edges = pd.DataFrame(data=[],
                         columns=['id1', 'id2', 'weight'])

    for i in range(n):
        for j in range(i+1, n):
            p1 = participants[i]
            p2 = participants[j]

            # year_of_study
            year_weight = 5 - abs(YEAR_TO_NUM[p1.year_of_study] - YEAR_TO_NUM[p2.year_of_study])

            # interests
            interests_weight = 0
            for a in p1.interests:
                for b in p2.interests:
                    if a == b: interests_weight += 1

            # preferred_role
            role_weight = 0
            for a in p1.preferred_role:
                for b in p2.preferred_role:
                    if a != b: role_weight += 1

            # friend_registration
            friend_weight = 0
            if p1.id in p2.friend_registration: friend_weight += 5
            if p2.id in p1.friend_registration: friend_weight += 5

            # interest_in_challenges
            challenges_weight = 0
            for a in p1.interest_in_challenges:
                for b in p2.interest_in_challenges:
                    if a == b: challenges_weight += 1

            # preferred_languages
            languages_weight = 0
            for a in p1.preferred_languages:
                for b in p2.preferred_languages:
                    if a == b: languages_weight = max(languages_weight, 1)

            total_weight = (
                year_mult * year_weight
                + interests_mult * interests_weight
                + preferred_role_mult * role_weight
                + friend_mult * friend_weight
                + challenges_mult * challenges_weight
                + languages_mult * languages_weight
            )

            edges.loc[len(edges)] = [p1.id, p2.id, total_weight]

    max_weight = max(edges['weight'])
    if max_weight != 0.0: edges['weight'] = edges['weight'] / max_weight
    edges = edges[edges['weight'] > edge_threshold]

    # clusters
    edges2 = edges.copy()
    edges2['weight'] = 1 / edges['weight']

    graph2 = nx.Graph()
    graph2.add_nodes_from(nodes["id"])
    graph2.add_edges_from(zip(edges2['id1'], edges2['id2'], edges2[['weight']].to_dict(orient='records')))

    clf = KMeansConstrained(
        n_clusters=n_clusters,
        size_min=2,
        size_max=4,
        random_state=0
    )

    adj_matrix = nx.to_numpy_array(graph2)
    clusters = clf.fit_predict(adj_matrix)
    nodes['color'] = clusters

    print(clusters)

    # visuals
    nodes['color'] = nodes['color'].copy().apply(cluster_to_color, args=(n_clusters,))
    nodes['size'] = 20

    edges['color'] = edges['weight'].apply(percentage_to_color)
    edges['weight'] = round(edges['weight'] * edge_max_width, 0)

    graph = nx.Graph()
    graph.add_nodes_from(zip(nodes["id"], nodes[['label', 'color', 'size']].to_dict(orient="records")))
    graph.add_edges_from(zip(edges['id1'], edges['id2'], edges[['weight', 'color']].to_dict(orient='records')))

    return graph
