import networkx as nx
import pandas as pd
import pytest

from src.algorithms.graphs import remove_cycles
from utils.loading import get_file


@pytest.mark.benchmark(group="Remove Cycle")
def test_remove_cycle(benchmark):
    file_dir = 'benchmarks/data/input/'
    file_name = 'gigante.csv'
    file_path = get_file(file_dir, file_name)
    data = pd.read_csv(file_path)
    G = nx.from_pandas_edgelist(
        data,
        source='Source',
        target='Target',
        create_using=nx.DiGraph(),
        edge_attr=["pln_date"]
    )

    @benchmark
    def remove_cycle_with_gigante():
        remove_cycles(G)
