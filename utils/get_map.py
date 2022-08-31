import os
import sys

import networkx as nx
import pandas as pd
import glob
import time
import datetime

from numpy import savetxt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
local_path = os.path.abspath(os.path.dirname(__file__))
output_path = os.path.join(local_path, "../tests/data/output/")
local_path = os.path.join(local_path, "../benchmarks/data/input/")

if __name__ == "__main__":
    from src.algorithms.edge_weights import calculate_splc_optimized
    from src.algorithms.dag import get_syncs, add_artificial_source_sync, remove_anomalies
    from src.algorithms.paths import main_path

    graphs_files = glob.glob(os.path.join(local_path, '*without_cycles.csv'))
    print(*graphs_files, sep='\n')
    for file_name in graphs_files:
        data = pd.read_csv(file_name)
        G = nx.from_pandas_edgelist(
            data,
            source='Source',
            target='Target',
            create_using=nx.DiGraph()
        )
        nx.set_node_attributes(G, pd.Series(data.pln_date.values, index=data.Source).to_dict(), "pln_date")
        edges_removed = remove_anomalies(G)
        add_artificial_source_sync(G)
        syncs = get_syncs(G)
        start = time.process_time()
        calculate_splc_optimized(G, syncs)
        end = time.process_time() - start
        print("\nRunning time of {}: \t {}".format(file_name, str(datetime.timedelta(seconds=end))))
        print("{} anomalous citations removed".format(edges_removed))
        path = main_path(G)
        print(*path, sep=" -> ")
        new_file_name = file_name.split("input/", 1)[1]
        new_file_name = new_file_name.replace("_without_cycles.csv", ".txt")
        new_file_name = "main_path_" + new_file_name

        savetxt(os.path.join(output_path, new_file_name), path, fmt="%s", newline='->')




