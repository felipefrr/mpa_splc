# Importando todas as funções que precisamos:
from src.algorithms.edge_weights import calculate_splc_optimized
from src.algorithms.dag import get_syncs, add_artificial_source_sync, remove_anomalies, remove_cycles
from src.algorithms.paths import main_path

import os
import pandas as pd
import neetwork as nx

# ------ Como carregar um arquivo? ------
"""
Precisaremos do endereço do arquivo de interesse no formato CSV e em seguida lê-lo
em um Pandas Dataframe.
"""
# Encontra o caminho para o diretório do arquivo que estamos rodando (mpa_starting_pack.py)
local_path = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(local_path, 'benchmarks/data/input/gigante_with_cycles.csv')

# Lê o CSV
data = pd.read_csv(file_path)

# Cria um grafo (do tipo nx.Digraph) através do Dataframe
G = nx.from_pandas_edgelist(
    data,
    source='Source',
    target='Target',
    create_using=nx.DiGraph()
)

# Adicionamos a informação da pln_date, salvamos essa informação em seu respectivo nó:
nx.set_node_attributes(G, pd.Series(data.pln_date.values, index=data.Source).to_dict(), "pln_date")

# ------ Como remover o ciclo? ------
# Para remover ciclo basta chamar a função remove_cycles da remove_cycles em algorithms/dag.py
edges_removes = remove_cycles(G)
# Essa função remove os ciclos inplace.



# ------ Como printar o SPLC? ------
# Antes de printar o SPLC, precisamos calculá-lo primeiro.

# Adcionamos um source e um sync artificial para simplificar a busca.
add_artificial_source_sync(G)


syncs = get_syncs(G)

# Calcularemos o SPLC.
calculate_splc_optimized(G, syncs)
# Em calculate_splc_optimized salvamos a informação do SPLC dentro do próprio no, portanto para acessá-la precisaremos de uma hash.


# Para printar o SPLC, precisamores iterar sobre todas as arestas do grafo e mostrar seus valores:
edges = list(map(list, G.edges()))
for edge in edges:
    print(G[edge[0]][edge[1]]["SPLC"])

# ------ Como calcular o Main Path? ------
path = main_path(G)

# Como printar o main path?
print(*path, sep=" -> ")

