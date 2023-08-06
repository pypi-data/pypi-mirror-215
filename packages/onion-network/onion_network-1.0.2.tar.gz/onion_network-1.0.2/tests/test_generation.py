from onion_network import onion_graph_from_degree_sequence
import networkx as nx
import pytest


@pytest.fixture
def degree_sequence():
    degree_sequence = sorted(
        [
            3,
            3,
            3,
            9,
            9,
            3,
            3,
            4,
            6,
            3,
            12,
            3,
            7,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            15,
            15,
            3,
            3,
            5,
            3,
            3,
            3,
            13,
            3,
            3,
            7,
            8,
            3,
            3,
            3,
            4,
            3,
            11,
            3,
            3,
            3,
            3,
            15,
            3,
            3,
            15,
            3,
            6,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            15,
            3,
            3,
            5,
            3,
            12,
            3,
            8,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            15,
            3,
            3,
            3,
        ]
    )
    return degree_sequence


def test_onion_graph_respects_degree(degree_sequence):
    G = onion_graph_from_degree_sequence(degree_sequence, seed=1)
    G_degree = sorted([x for _, x in G.degree()])
    assert all([d1 == d2 for d1, d2 in zip(degree_sequence, G_degree)])


def test_assortativity(degree_sequence):
    """Onion networks should be assortative for alpha big enough: same degree nodes should be connected to similar degree nodes in majority."""
    for i in range(100):
        G = onion_graph_from_degree_sequence(degree_sequence, seed=i, alpha=100)
        assert nx.degree_assortativity_coefficient(G) > 0
