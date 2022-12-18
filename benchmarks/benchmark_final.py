# pytest --benchmark-timer=time.process_time --benchmark-save=final --benchmark-warmup=OFF --benchmark-warmup-iterations=0 --benchmark-min-rounds=1 --benchmark-save-data --benchmark-verbose benchmarks/benchmark_final.py
import networkx as nx
import pandas as pd
import pytest
from src.algorithms.edge_weights import calculate_splc_optimized
from src.algorithms.dag import get_syncs
from src.algorithms.paths import main_path
from utils.loading import get_file


class HugeGraph:
    def __init__(self):
        file_dir = 'benchmarks/data/input/'
        file_name = '392k_nodes_642k_edges_without_cycles.csv'
        file_path = get_file(file_dir, file_name)
        data = pd.read_csv(file_path)
        self.G1 = nx.from_pandas_edgelist(
            data,
            source='Source',
            target='Target',
            create_using=nx.DiGraph(),
            edge_attr=["pln_date"]
        )
        self.syncs = get_syncs(self.G1)

        file_name = '844k_nodes_1.6m_edges_without_cycles.csv'
        file_path = get_file(file_dir, file_name)
        data = pd.read_csv(file_path)
        self.G2 = nx.from_pandas_edgelist(
            data,
            source='Source',
            target='Target',
            create_using=nx.DiGraph(),
            edge_attr=["pln_date"]
        )
        self.syncs2 = get_syncs(self.G2)

        file_name = 'gigante_without_cycles.csv'
        file_path = get_file(file_dir, file_name)
        data = pd.read_csv(file_path)
        self.G3 = nx.from_pandas_edgelist(
            data,
            source='Source',
            target='Target',
            create_using=nx.DiGraph(),
            edge_attr=["pln_date"]
        )
        self.syncs3 = get_syncs(self.G3)


@pytest.fixture()
def di_G():
    return HugeGraph()


def test_main_path_f1(benchmark, di_G):
    @benchmark
    def file1_23n_33e():
        calculate_splc_optimized(di_G.G1, di_G.syncs)
        main_path(di_G.G1)


def test_main_path_f2(benchmark, di_G):
    @benchmark
    def file1_23n_33e():
        calculate_splc_optimized(di_G.G2, di_G.syncs2)
        main_path(di_G.G2)


def test_main_path_f3(benchmark, di_G):
    @benchmark
    def file1_844n_1me():
        calculate_splc_optimized(di_G.G3, di_G.syncs3)
        main_path(di_G.G3)
