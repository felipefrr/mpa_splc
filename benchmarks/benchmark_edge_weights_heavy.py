import networkx as nx
import pandas as pd
import pytest

from src.algorithms.edge_weights import calculate_splc_fast, calculate_splc_optimized
from src.algorithms.dag import get_syncs, get_sources
from utils.loading import get_file


class HugeGraph:
    def __init__(self):
        file_dir = 'benchmarks/data/input/'
        file_name = 'gigante_without_cycles.csv'
        file_path = get_file(file_dir, file_name)
        data = pd.read_csv(file_path)
        self.G = nx.from_pandas_edgelist(
            data,
            source='Source',
            target='Target',
            create_using=nx.DiGraph(),
            edge_attr=["pln_date"]
        )
        self.sources = get_sources(self.G)
        self.syncs = get_syncs(self.G)


@pytest.fixture()
def di_G():
    return HugeGraph()


@pytest.mark.benchmark(group="SPLC with heavy file")
def test_calc_splc_fast(benchmark, di_G):
    @benchmark
    def splc_fast():
        calculate_splc_fast(di_G.G, di_G.sources, di_G.syncs)


@pytest.mark.benchmark(group="SPLC with heavy file")
def test_calc_splc_optimized(benchmark, di_G):
    @benchmark
    def splc_fast():
        calculate_splc_optimized(di_G.G, di_G.syncs)
