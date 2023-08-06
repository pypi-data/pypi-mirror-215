import networkx as nx
from collections import defaultdict
from matplotlib import cm


def plot_onion(G: nx.Graph, cmap: str = "tab20c"):

    cmap = cm.get_cmap(cmap)

    layers = get_layers(G)
    degree_map = {node: degree for node, degree in G.degree()}

    # Node position
    pos_tot = {}
    for layer, nodes in layers.items():
        pos_tot = {
            **pos_tot,
            **nx.circular_layout(nx.subgraph(G, nodes), scale=1 / layer, center=None),
        }

    # Edge style
    edge_style = []
    for node_1, node_2 in G.edges():
        if degree_map[node_1] == degree_map[node_2]:
            edge_style.append("-")
        else:
            edge_style.append(":")

    # Edge color
    edge_color = []
    for node_1, node_2 in G.edges():
        if degree_map[node_1] == degree_map[node_2]:
            edge_color.append(cmap(degree_map[node_1]))
        else:
            edge_color.append(cmap(-1))

    plot = nx.draw(
        G,
        pos_tot,
        style=edge_style,
        node_color=[cmap(degree_map[x]) for x in G.nodes()],
        node_size=[degree_map[x] * 2**5 for x in G.nodes()],
        connectionstyle="arc3,rad=0.2",
        arrows=True,
        edge_color=edge_color,
    )

    return plot


def get_layers(G: nx.Graph) -> dict:
    groups = defaultdict(list)
    for node, degree in G.degree():
        groups[degree].append(node)
    return groups
