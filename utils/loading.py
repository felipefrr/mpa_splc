import networkx as nx
import pandas as pd
import os.path
import glob

__all__ = [
    "get_all_input_graphml_files_path",
    "get_all_output_csv_files_path",
    "load_graphml_file",
    "load_csv_file"
]


def get_all_input_graphml_files_path() -> list:
    """Returns a lists containing all the path of
       all .graphml files presented in tests/data/input.

        Returns
        -------
        input_files : list
            An list containing file paths.
    """
    local_path = os.path.abspath(os.path.dirname(__file__))
    test_data_path = os.path.join(local_path, "../tests/data/input/")
    input_files = glob.glob(test_data_path + "*.graphml")
    return input_files


def get_all_output_csv_files_path() -> list:
    """Returns a lists containing all the path of
       all .csv files presented in tests/data/output.

        Returns
        -------
        input_files : list
            An list containing file paths.
    """
    local_path = os.path.abspath(os.path.dirname(__file__))
    test_data_path = os.path.join(local_path, "../tests/data/output/")
    input_files = glob.glob(test_data_path + "*.csv")
    return input_files


def load_graphml_file(file_path):
    """Returns the graph from a .graphml file loaded in a NetworkX graph.

        Parameters
        ----------
        file_path : string
            A string with the absolute path of the .graphml file.


        Returns
        -------
        G : graph
            A NetworkX graph.
    """
    return nx.read_graphml(file_path)


def load_csv_file(file_path):
    """Returns the graph from a .csv loaded in a NetworkX graph.

        Parameters
        ----------
        file_path : string
            A string with the absolute path of the .csv file.


        Returns
        -------
        G : graph
            A NetworkX graph.
    """

    data = pd.read_csv(file_path)
    G = nx.from_pandas_edgelist(
                                data,
                                source='SOURCE',
                                target='TARGET',
                                create_using=nx.DiGraph(),
                                edge_attr=["SPC", "SPLC"]
    )
    return G
