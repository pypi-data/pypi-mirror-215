<h1  align="center">🧅 Onion Network </h1>

<img src="imgs/illustration.png" alt="banner" width="100%">

<p align="center">
<a href="https://github.com/SimonPop/onion_network/"><img alt="Project Version" src="https://img.shields.io/badge/version-1.0.0-blue"></a>
<a href="https://www.python.org"><img alt="Python Version 3.8" src="https://img.shields.io/badge/Python-3.8-blue.svg?style=flat&logo=python&logoColor=white"></a>
<a href="https://github.com/SimonPop/onion_network/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://badge.fury.io/py/onion-network"><img src="https://badge.fury.io/py/onion-network.svg" alt="PyPI version" height="18"></a>
</p>

Onion-structured networks are special kinds of scale-free networks with special topologies. 

They tend to possess a high degree [assortativity](https://en.wikipedia.org/wiki/Assortativity). It makes it possible to decompose them into layers of same-degree nodes, hence the name.

This property gives them strong resilience to [node deletion](https://en.wikipedia.org/wiki/Node_deletion) attacks.

This library can help you explore these networks, giving access to both a generation and visualization method. 

## Algorithm

A generative algorithm producing synthetic scale-free networks with onion structure is implemented as described in the paper: [Onion structure and network robustness](https://arxiv.org/abs/1108.1841).

> Note: This algorithm can fail under certain circumstances. Therefore a `max_trial` number has been added so that the process can be tried different times until a viable solution is found.

### Visualization

A side module allows plotting the generated graphs, radially separating onion layers.

## Usage

### Installation

You can install the package using `pip`.

```shell
pip install onion-network
```

### Example

```python
# Example usage of the onion generation and plotting.
from onion_network import plot_onion, onion_graph
G = onion_graph(n=100, gamma=2.5, alpha=3, max_trial=100)
plot_onion(G, cmap="tab20b")
```

<img src="imgs/example.png" alt="banner" width="50%" style="display:block;margin-left: auto;margin-right: auto;">


## References

### Papers

Chan, H., & Akoglu, L. (2016). Optimizing network robustness by edge rewiring : A general framework. Data Mining and Knowledge Discovery, 30(5), 1395‑1425. https://doi.org/10.1007/s10618-015-0447-5
Chujyo, M., & Hayashi, Y. (2022). Adding links on minimum degree and longest distance strategies for improving network robustness and efficiency. PLOS ONE, 17(10), e0276733. https://doi.org/10.1371/journal.pone.0276733
Hayashi, Y. (2018). A new design principle of robust onion-like networks self-organized in growth. Network Science, 6(1), 54‑70. https://doi.org/10.1017/nws.2017.25
Liu, X., Sun, S., Wang, J., & Xia, C. (2019). Onion structure optimizes attack robustness of interdependent networks. Physica A: Statistical Mechanics and Its Applications, 535, 122374. https://doi.org/10.1016/j.physa.2019.122374
Louzada, V. H. P., Daolio, F., Herrmann, H. J., & Tomassini, M. (2013). Smart Rewiring for Network Robustness. Journal of Complex Networks, 1(2), 150‑159. https://doi.org/10.1093/comnet/cnt010
Wu, Z.-X., & Holme, P. (2011, août 9). Onion structure and network robustness. ArXiv.Org. https://doi.org/10.1103/PhysRevE.84.026106

### Blog article

[The Onion Topology](https://simonpop.github.io/the-onion-topology.html)