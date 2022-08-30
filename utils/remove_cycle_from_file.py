# main.py

import os
import sys

import networkx as nx
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
local_path = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    local_path = os.path.join(local_path, "../benchmarks/data/input/")
    print(local_path)
    from src.algorithms.dag import remove_cycles
    n_files = len(sys.argv)
    for i in range(1, n_files):
        file_name = sys.argv[i]
        file_path = os.path.join(local_path, file_name)
        data = pd.read_csv(file_path)
        G = nx.from_pandas_edgelist(
            data,
            source='Source',
            target='Target',
            create_using=nx.DiGraph(),
            edge_attr="pln_date"
        )
        remove_cycles(G)
        df = nx.to_pandas_dataframe(G, nodelist=["Source", "Target", "pln_date"])
        df.to_csv(file_path.replace("with", "without"), sep=',')



