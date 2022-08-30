import networkx as nx
import pandas as pd
import pytest
from src.algorithms.edge_weights import calculate_splc_optimized
from src.algorithms.dag import get_syncs, remove_cycles
from src.algorithms.paths import main_path
from utils.loading import get_file


class HugeGraph:
    def __init__(self):
        file_dir = 'benchmarks/data/input/'
        file_name = '392k_nodes_642k_edges_without_cycles.csv'
        file_path = get_file(file_dir, file_name)
        data = pd.read_csv(file_path)
        self.G = nx.from_pandas_edgelist(
            data,
            source='Source',
            target='Target',
            create_using=nx.DiGraph(),
            edge_attr=["pln_date"]
        )
        self.syncs = get_syncs(self.G)

        file_name = '844k_nodes_1.6m_edges_without_cycles.csv'
        file_path = get_file(file_dir, file_name)
        data = pd.read_csv(file_path)
        self.G1 = nx.from_pandas_edgelist(
            data,
            source='Source',
            target='Target',
            create_using=nx.DiGraph(),
            edge_attr=["pln_date"]
        )
        self.syncs1 = get_syncs(self.G1)


@pytest.fixture()
def di_G():
    return HugeGraph()


@pytest.mark.benchmark(group="Main Path Heavy")
def test_main_path_f1(benchmark, di_G):
    @benchmark
    def main_path_heavyfile1():
        calculate_splc_optimized(di_G.G, di_G.syncs)
        main_path(di_G.G)


@pytest.mark.benchmark(group="Main Path Heavy")
def test_main_path_f2(benchmark, di_G):
    @benchmark
    def main_path_heavyfile2():
        calculate_splc_optimized(di_G.G1, di_G.syncs1)
        main_path(di_G.G1)
