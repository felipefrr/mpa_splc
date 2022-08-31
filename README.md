![Tests](https://github.com/felipefrr/map_splc/actions/workflows/tests.yml/badge.svg) [![codecov](https://codecov.io/gh/felipefrr/map_splc/branch/main/graph/badge.svg?token=O1ZP96FUIM)](https://codecov.io/gh/felipefrr/map_splc)

# Main Path Analysis

Repository for made with the intent of providing optimal implementations of Main Path Analysis (MPA) with Search Path Link Count (SPLC). The work done here is proof of concept for my undergraduation thesis at the Institute of Mathematics and Statistics (IME) in University of São Paulo (USP).
We have the intent of further adding these algorithms implementations in the NetworkX library.
We're covering the following aspects of this project: Unit Tests, Code Coverage, Linting and Type Checking.

### 📝💻 Todo
- [⏳] Write the unit tests for remaining methods:
  - `add_artificial_source_sync`
  - `simplify`
  - `remove_anomalies`
  - `main_path`
- [⏳] Improve unit tests implementation
- [✔️] Implement function add artificial source and sync vertex
- [✔️] Implement Main Path Search
- [✔️] Migrate all the code of rdurelli/splc_main_path to this repo
- [✔️] Write the unit tests for `convert_graph_to_dag`
- [✔️] Write the unit tests
- [✔️] Implement IO functions
- [✔️] Implement my own version of SPLC
- [✔️] Implement cycle removal. P.S.: we need to make a discussion about the most suitable method considering your graph structure and magnitude of the set cycles. It was implemented in the `convert_graph_to_dag`, considering the heuristics of removing the edge with the least `pln_date`.

### Implementation notes
The `pln_date` is a source node attribute, not an edge attribute, but setting it as an edge attribute seems to not impact the logic. However, I'm not sure, we will need further inspection.

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

# If you want to benchmark the main path with the heavy files `benchmarks/data/input/392k_nodes_642k_edges_without_cycles.csv` and `benchmarks/data/input/844k_nodes_1.6m_edges_without_cycles.csv`.
make heavy-benchmark-main-path
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
The benchmark in the file `tests_path_functions.py` correspond to the function `main_path`. You can run it with the following command:
```
pytest --benchmark-verbose benchmarks/benchmark_graph_functions.py
```
The benchmark in the file  `tests_path_functions_heavy.py` with the large graph `benchmarks/data/input/gigante_without_cycles.csv`. You can run it with the following command:
```
pytest --benchmark-verbose benchmarks/tests_path_functions_heavy.py
```

## Utils

### Main Path
The script `get_map.py` at `utils` was made to perform the Main Path Analysis in the all files with the suffix `_without_cycles.csv` at the folder `benchmarks/data/input`, this file must have the `.csv` header "Source,Target,pln_date".

You can run the script by (check if you activated the virtual environment):
```
cd utils
python get_map.py
```
E.g., the expected output is as it follows:
```
Running time of /home/frrr/workplace/map_splc/utils/../benchmarks/data/input/844k_nodes_1.6m_edges_without_cycles.csv: 	 0:00:18.144553
1967 anomalous citations removed
source -> US20160197204A1 -> US20140224307A1 -> US20120211068A1 -> US20120103403A1 -> US20120211071A1 -> US20100282288A1 -> US20100012175A1 -> US20100122764A1 -> US20100012174A1 -> US20100116327A1 -> US20100093127A1 -> US20090188546A1 -> US20090288703A1 -> US20080245409A1 -> US20050274411A1 -> US20040079408A1 -> US20040065363A1 -> US6316715B1 -> US5407491A -> sync
```

### Remove Cycle
The script `remove_cycle_from_file.py` at `utils` remove cycles from graphs in the `with_cycles.csv` extension at the `benchmarks/data/input` folder and export to the same directory without the cycles. 
Usage:
```
remove_cycle_from_file.py graph1_with_cycle.csv graph2_with_cycle.csv ... graphn_with_cycle.csv

Remove cycles from graphs

Positional arguments:
 with_cycle.csv        .csv file name.
```
Example:
```
cd utils
python remove_cycle_from_file.py 392k_nodes_642k_edges_with_cycles.csv 844k_nodes_1.6m_edges_with_cycles.csv
```
The expected output is two files`392k_nodes_642k_edges_without_cycles.csv` and `844k_nodes_1.6m_edges_without_cycles.csv` created in the `benchmarks/data/input` folder.


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