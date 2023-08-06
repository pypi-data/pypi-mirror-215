from typing import List
import networkx as nx
import random
from networkx.utils.random_sequence import powerlaw_sequence


def onion_graph(
    n: int = 100,
    seed: int = None,
    gamma: float = 2.5,
    alpha: float = 3.0,
    max_trial: int = 100,
    min_degree: int = 0,
    max_degree: int = float("inf"),
):
    """Generates an onion-structured graph.

    Args:
        seed (_type_, optional): _description_. Defaults to None.

    References
    ----------
    ..  [1] Wu, Z.-X., & Holme, P. (2011). Onion structure and network robustness. Physical Review E, 84(2), 026106. https://doi.org/10.1103/PhysRevE.84.026106
    """

    # Sample degrees from a power law. Sort them increasingly.
    degree_sequence = [d for d in powerlaw_sequence(n, exponent=gamma, seed=seed)]
    degree_sequence = [min(d, max_degree) for d in degree_sequence]
    degree_sequence = [max(d, min_degree) for d in degree_sequence]
    degree_sequence = [int(d) for d in degree_sequence]

    # We need a pair degree sequence or degree greater than the number of vertex, or the graph would be impossible to generate.
    while not nx.is_graphical(degree_sequence):
        if not seed is None:
            raise ValueError(
                "This seed does not allow for a valid degree sequence. Please try another seed or run again without seed."
            )
        degree_sequence = [d for d in powerlaw_sequence(n, exponent=gamma, seed=seed)]
        degree_sequence = [min(d, max_degree) for d in degree_sequence]
        degree_sequence = [max(d, min_degree) for d in degree_sequence]
        degree_sequence = [int(d) for d in degree_sequence]
        max_trial = max_trial - 1

    if seed is None and max_trial > 0:
        try:
            # Try with this degree sequence with half max trial. Reserve other half in case this degree sequence is failing.
            G = onion_graph_from_degree_sequence(
                degree_sequence, alpha=alpha, seed=seed, max_trial=max_trial // 2
            )
        except:
            # Try with another degree sequence.
            G = onion_graph(n, seed, gamma, alpha, max_trial=max_trial // 2)
    else:
        # Re-trying is useless since the seed is defining the degree sequence.
        G = onion_graph_from_degree_sequence(
            degree_sequence, alpha=alpha, seed=seed, max_trial=max_trial
        )

    return G


def onion_graph_from_degree_sequence(
    degree_sequence: List[int],
    seed: int = None,
    alpha: float = 3.0,
    max_trial: int = 100,
):
    random.seed(seed)

    if not nx.is_graphical(degree_sequence):
        raise ValueError(
            "This degree sequence is not graphical. It would be impossible to generate an onion structure with it."
        )

    degree_sequence = sorted(degree_sequence, reverse=False)

    # Store trial number.
    initial_max_trial = max_trial

    # Initialize an empty graph.
    G = nx.Graph()
    vertices = range(len(degree_sequence))

    # Declare data structure for building the graph.
    remaining_stub_list = degree_sequence.copy()

    for vertex, layer in enumerate(degree_sequence):
        stub_number = remaining_stub_list[vertex]
        for _ in range(stub_number):
            # Sample probability of connecting the current vertex to another vertex based assortativity equation, whether or not vertex has remaining stubs left and whether or not the link already exists in the graph.
            link_probabilities = [
                int(1 - G.has_edge(vertex, target_vertex))
                * int(remaining_stub_list[target_vertex] > 0)
                * _link_probability(layer, target_layer, alpha=alpha)
                for target_vertex, target_layer in enumerate(degree_sequence)
            ]

            # Prevent self loops by setting probability of choosing itself to 0.
            link_probabilities[vertex] = 0

            if sum(link_probabilities) > 0:
                # Sample the node to connect using link probabilities.
                target_vertex = random.choices(
                    vertices, weights=link_probabilities, k=1
                )[0]

                G.add_edge(vertex, target_vertex)

                remaining_stub_list[vertex] = remaining_stub_list[vertex] - 1
                remaining_stub_list[target_vertex] = (
                    remaining_stub_list[target_vertex] - 1
                )

    # For all remaining stubs, we need to re-arange existing links to create new opportunities of connections.

    # Create a pool of vertices (e.g. [0,3,2,1] -> [1,1,1,2,2,3]).
    remaining_stub_pool = [
        vertex
        for vertex, remaining_stubs in enumerate(remaining_stub_list)
        for _ in range(remaining_stubs)
    ]

    if len(remaining_stub_pool) % 2 == 1:
        raise ValueError(
            "Degree incoherency. The algorithm does not allow generation for that topology."
        )

    while len(remaining_stub_pool) and max_trial > 0:
        (index_1, vertex_1), (index_2, vertex_2) = random.sample(
            list(enumerate(remaining_stub_pool)), k=2
        )
        try:
            G = _swap_links(vertex_1, vertex_2, G)
            for index in sorted((index_1, index_2), reverse=True):
                del remaining_stub_pool[index]
        except:
            # This specific pair of stubs could never be inserted. Try a new one.
            pass

        max_trial = max_trial - 1

    if max_trial == 0:
        raise ValueError(
            f"""
            Maximum trial number {initial_max_trial} exceeded. 
            You can try running again and/or trying with:
            - Another seed.
            - Another degree sequence.
            - A larger maximum trial number.
        """
        )

    return G


def _link_probability(degree_i: int, degree_j: int, alpha: float) -> float:
    return 1 / (1 + alpha * abs(degree_i - degree_j))


def _swap_links(vertex_1: int, vertex_2: int, G: nx.Graph) -> nx.Graph:
    """Disconnect a link in  order to create to alternative links."""

    # Only allow swap for nodes that aren't already connected.
    edge_pool = [e for a, b in G.edges() for e in [(a, b), (b, a)]]
    edge_pool = [
        (a, b)
        for a, b in edge_pool
        if not G.has_edge(vertex_1, a)
        and not G.has_edge(vertex_2, b)
        and vertex_2 != b
        and vertex_1 != a
    ]
    if len(edge_pool) == 0:
        raise ValueError(
            f"Impossible to find edges to swap {vertex_1} and {vertex_2} with. All candidates create either self loops or multi-edges."
        )

    vertex_1_target, vertex_2_target = random.choice(edge_pool)

    # Swap edges.
    G.remove_edge(vertex_1_target, vertex_2_target)
    G.add_edge(vertex_1, vertex_1_target)
    G.add_edge(vertex_2, vertex_2_target)

    return G
