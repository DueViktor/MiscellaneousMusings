"""Exercise given by Michele Coscia in the course Advanced Network Analysis at ITU, Autumn 2023."""

from tqdm import tqdm
import copy
import random
from math import log as ln
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def create_graph(n: int, k: int) -> nx.Graph:
    
    assert n > k > ln(n) > 1, "Ensure that n > k > ln(n) > 1."

    # We start with a ring of n vertices, ...
    G = nx.Graph()
    G.add_nodes_from(range(n))

    # ... each connected to its k nearest neighbours by undirected edges.
    for i in range(n):
        for j in range(i + 1, i + k // 2 + 1):
            G.add_edge(i, j % n)

    # minor extension assert that the degree of all nodes are equal to k
    assert all(deg == k for _, deg in G.degree()), "All nodes must have degree k."

    return G


def rewire_with_probability(G: nx.Graph, p: float) -> nx.Graph:
    """Rewiring can be done in many ways. Based on figure 1 it seems
    they are only rewiring one of the endpoints of the edge. I'll do the same"""

    # assert valid probability
    assert 0 <= p <= 1, f"p must be between 0 and 1, but was {p}."

    # create a copy of the graph
    graph: nx.Graph = copy.deepcopy(G)

    def is_valid_edge(u: int, v: int, G:nx.Graph) -> bool:
        """Check if an edge between u and v is valid."""
        return u != v and not G.has_edge(u, v)

    # For each edge (u, v) in the graph, rewire the edge with probability p
    for u, v in graph.edges:
        rewire: bool = p > random.random()

        if rewire:
            while True:
                new_v: int = random.choice(list(graph.nodes))
                if is_valid_edge(u, new_v, graph):
                    break

            graph.remove_edge(u, v)
            graph.add_edge(u, new_v)

    return graph

def figure_1():
    G: nx.Graph = create_graph(10, 4)

    ps = np.array([0, 0.25, 1.0])
    titles = ["Regular\n$p = 0$", f"Small-world\n$p = {ps[1]}$", "Random\n$p = 1$"]

    fig, ax = plt.subplots(1, len(ps), figsize=(12, 4))

    for i, p in enumerate(ps):
        rewired: nx.Graph = rewire_with_probability(G, p)
        
        # Use connectionstyle only for the first plot, omit it otherwise
        nx.draw(
            rewired,
            pos=nx.circular_layout(rewired),
            with_labels=False,
            node_color='black',
            edge_color='black',
            node_size=150,
            width=0.8,
            ax=ax[i],
        )
        
        ax[i].set_title(titles[i])
        ax[i].set_axis_off()  # Turn off the axis

    plt.tight_layout()
    plt.savefig("assets/figure_1.png", dpi=300)
    plt.clf()

def figure_2():
    def get_metrics(G: nx.Graph) -> Tuple[float, float]:
        L_g = nx.average_shortest_path_length(G)
        C_g = nx.average_clustering(G)
        return L_g, C_g

    ps = np.logspace(-4, 0, num=14)

    G: nx.Graph = create_graph(1000, 10)

    L_0, C_0 = get_metrics(G)

    Ls, Cs = [], []
    for p in tqdm(ps):
        Ls_p = []
        Cs_p = []
        for _ in range(20):
            G_rewired = rewire_with_probability(G, p)
            L_g, C_g = get_metrics(G_rewired)
            Ls_p.append(L_g / L_0)
            Cs_p.append(C_g / C_0)

        Ls.append(sum(Ls_p) / len(Ls_p))
        Cs.append(sum(Cs_p) / len(Cs_p))

    plt.figure(figsize=(8, 8))  
    plt.scatter(ps, Ls, label="L(p)/L(0)")
    plt.scatter(ps, Cs, label="C(p)/C(0)")
    plt.xscale("log")
    plt.legend()
    plt.tight_layout()

    plt.savefig("assets/figure_2.png")
    plt.clf()

if __name__ == "__main__":
    figure_1()
    figure_2()