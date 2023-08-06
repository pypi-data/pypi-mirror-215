<h1  align="center">🧅 Onion Network </h1>

<img src="imgs/illustration.png" alt="banner" width="100%">

<p align="center">
<a href="https://github.com/SimonPop/onion_network/"><img alt="Project Version" src="https://img.shields.io/badge/version-1.0.0-blue"></a>
<a href="https://www.python.org"><img alt="Python Version 3.8" src="https://img.shields.io/badge/Python-3.8-blue.svg?style=flat&logo=python&logoColor=white"></a>
<a href="https://github.com/SimonPop/onion_network/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Onion-structured networks are special kinds of scale-free networks with a special topologies. They can be decomposed into layers of similar degree nodes.

This property gives them a strong resilience to node failure/removal attacks.

This library can help you explore these networks, giving access to both a generation and visualization method. 

## Usage

### Installation

TODO

> Note: [(Wu & Holme, 2011)](https://arxiv.org/abs/1108.1841) describe a generation algorithm in their paper. This algorithm is implemented in this  repository. This algorithm can fail under certain circumstances. Therefore a `max_trial` number has been added so that the process can be tried different times.

### Example

```python
from onion_network import onion_graph, plot_onion

G = onion_graph(n=100, gamma=2.5, alpha=3., max_trial=1000)

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