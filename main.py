import pandas as pd

from lib import parse_stamp, get_nodes, get_vs, get_neighbour_components, assign_ids, construct_b, construct_A, get_components, compute_MNA

# parse datafile into components
df = pd.read_csv("./data/scam_circuit.csv")
x = compute_MNA(df, print_eqs=True)
