# from "python -m pip install cupy" -- MUST HAVE CUDA SETUP
import cupy as cp
import cupyx.scipy.sparse as cp_sparse
import pandas as pd

from lib import (
    parse_stamp,
    get_nodes,
    get_vs,
    get_neighbour_components,
    assign_ids,
    construct_b,
    construct_A,
    get_components,
)


def compute_MNA(df, print_eqs=False):
    components = get_components(df)
    nodes = get_nodes(components)

    # get unknown ivs
    voltage_sources = get_vs(components)
    num_nodes = len(nodes)

    # generate b matrix, and initialize zero-filled A-matrix
    b = construct_b(voltage_sources, num_nodes)
    A = construct_A(b, components, voltage_sources, num_nodes)

    cupy_A = cp_sparse.csr_matrix(A)
    cupy_b = cp.asarray(b)
    cupy_x = cp_sparse.linalg.lsqr(cupy_A, cupy_b)[0]

    if print_eqs:
        print("---" * A.shape[0], "\n", cupy_A, "\n", "---" * A.shape[0])
        print(cupy_x)
        print(cupy_b)

    return cp.asnumpy(cupy_x)


# parse datafile into components
df = pd.read_csv("./data/scam_circuit.csv")
x = compute_MNA(df, print_eqs=True)
