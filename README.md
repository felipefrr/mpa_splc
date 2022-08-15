![Tests](https://github.com/felipefrr/map_splc/actions/workflows/tests.yml/badge.svg) [![codecov](https://codecov.io/gh/felipefrr/map_splc/branch/main/graph/badge.svg?token=O1ZP96FUIM)](https://codecov.io/gh/felipefrr/map_splc)

# Main Path Analysis

Repository for made with the intent of providing optimal implementations of Main Path Analysis (MPA) with Search Path Link Count (SPLC). The work done here is proof of concept for my undergraduation thesis at the Institute of Mathematics and Statistics (IME) in University of São Paulo (USP).

### 📝💻 Todo
- [ ] Implement Main Path Search
- [ ] Write the unit tests for `convert_graph_to_dag`
- [50%] Migrate all the code of rdurelli/splc_main_path to this repo
- [✔️] Write the unit tests
- [✔️] Implement IO functions
- [✔️] Implement my own version of SPLC
- [✔️] Implement cycle removal. P.S.: we need to make a discussion about the most suitable method considering your graph structure and magnitude of the set cycles. It was implemented in the `convert_graph_to_dag`, considering the heuristics of removing the edge with the least `pln_date`.
- [ ] Create a good UI

## Getting started
```
# Clone this repo and change directory
git clone git@github.com:felipefrr/map_splc.git
cd map_splc

# Create a python virtualenv on your local machine (-B might be needed to execute)
make setup-venv -B

# Alternatively, built docker image
make setup

# Run the suite of tests and checks on your local machine
make checks

# Alternatively, run the suite of tests and checks on docker
make run-checks
```

## Our checks

We cover the following aspects of setting up a python project, including: Unit Tests, Code Coverage, Linting and Type Checking.


## Benchmark
```
pytest benchmarks/tests_edge_weights_functions.py
```

## 📃 Citation

```bibtex
@misc{map-splc-package,
  author = {Felipe Ferreira, Rafael Durelli},
  title = {Main Path Analysis - SPLC},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/felipefrr/map_splc/}}
}
```
