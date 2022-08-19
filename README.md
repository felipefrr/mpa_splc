![Tests](https://github.com/felipefrr/map_splc/actions/workflows/tests.yml/badge.svg) [![codecov](https://codecov.io/gh/felipefrr/map_splc/branch/main/graph/badge.svg?token=O1ZP96FUIM)](https://codecov.io/gh/felipefrr/map_splc)

# Main Path Analysis

Repository for made with the intent of providing optimal implementations of Main Path Analysis (MPA) with Search Path Link Count (SPLC). The work done here is proof of concept for my undergraduation thesis at the Institute of Mathematics and Statistics (IME) in University of São Paulo (USP).
We have the intent of further adding these algorithms implementations in the NetworkX library.
We're covering the following aspects of this project: Unit Tests, Code Coverage, Linting and Type Checking.

### 📝💻 Todo
- [ ] Implement function add artificial source and sync vertex. 
- [ ] Implement Main Path Search
- [ ] Create a good UI
- [50%] Migrate all the code of rdurelli/splc_main_path to this repo
- [✔️] Write the unit tests for `convert_graph_to_dag`
- [✔️] Write the unit tests
- [✔️] Implement IO functions
- [✔️] Implement my own version of SPLC
- [✔️] Implement cycle removal. P.S.: we need to make a discussion about the most suitable method considering your graph structure and magnitude of the set cycles. It was implemented in the `convert_graph_to_dag`, considering the heuristics of removing the edge with the least `pln_date`.

## Getting started
```
# Clone this repo and change directory
git clone git@github.com:felipefrr/map_splc.git
cd map_splc

# Create a python virtualenv on your local machine (-B might be needed to execute)
make setup-venv -B

# Run the suite of tests and checks on your local machine
make checks

# Alternatively, built docker image
make setup

# Run the suite of tests and checks on docker
make run-checks
```

## Benchmark

We have a very small graph set up for the benchmark in the file `tests_edge_weights_functions.py` and a very large (`benchmarks/data/input/gigante.csv`) in the `tests_edge_weights_heavy.py`. The `calculate_splc_fast` function is very greedy and does not handle large graphs, that's why we suppress its benchmarking at the `tests_edge_weights_heavy.py`. 
```
make performance-compare
```
The benchmark in the file `tests_graph_functions.py` correspond to the function `remove_cycles` with the large graph `benchmarks/data/input/gigante.csv`. You can run it with the following command:
```
pytest --benchmark-verbose benchmarks/benchmark_graph_functions.py
```

## 📃 Citation

```bibtex
@misc{map-splc-package,
  author = {Felipe Ferreira and Rafael Durelli and Alfredo Goldman vel Lejbman},
  title = {Main Path Analysis - SPLC},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/felipefrr/map_splc/}}
}
```