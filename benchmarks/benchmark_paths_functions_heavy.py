import networkx as nx
import pandas as pd
import pytest
from src.algorithms.edge_weights import calculate_splc_optimized
from src.algorithms.dag import get_syncs, remove_cycles
from src.algorithms.paths import main_path
from utils.loading import get_file


@pytest.mark.benchmark(group="Main Path Heavy")
def test_remove_cycle(benchmark):
    file_dir = 'benchmarks/data/input/'
    file_name = 'gigante_without_cycles.csv'
    file_path = get_file(file_dir, file_name)
    data = pd.read_csv(file_path)
    G = nx.from_pandas_edgelist(
        data,
        source='Source',
        target='Target',
        create_using=nx.DiGraph(),
        edge_attr=["pln_date"]
    )
    syncs = get_syncs(G)
    remove_cycles(G)
    calculate_splc_optimized(G, syncs)

    @benchmark
    def main_path_heavy():
        main_path(G)