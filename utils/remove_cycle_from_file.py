# main.py

import os
import sys
import time
import datetime

import networkx as nx
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
local_path = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    local_path = os.path.join(local_path, "../benchmarks/data/input/")
    from src.algorithms.dag import remove_cycles, simplify
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
        H = simplify(G)
        start = time.process_time()
        edges_to_remove = remove_cycles(H)
        G.remove_edges_from(edges_to_remove)
        end = time.process_time() - start
        print("\nRunning time of {}: \t {}".format(file_name, str(datetime.timedelta(seconds=end))))
        fh = open(file_path.replace("with", "without"), "wb")
        header = str.encode("Source,Target,pln_date\n")
        fh.write(header)
        nx.write_edgelist(G, fh, data=["pln_date"], delimiter=',')


