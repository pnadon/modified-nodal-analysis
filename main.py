import pandas as pd
import numpy as np
from scipy.sparse import linalg, csr_matrix, identity

# from "python -m pip install cupy" -- MUST HAVE CUDA SETUP
import cupy as cp
import cupyx.scipy.sparse as cp_sparse

from lib import parse_stamp, get_nodes, get_vs, get_neighbour_components, assign_ids

# parse datafile into components
df = pd.read_csv("./data/scam_circuit.csv")
components = []
for index, row in df.iterrows():
    components.append(parse_stamp(row))
    # similar components are numbered 1-n
    components = assign_ids(components)

# get nodes
nodes = get_nodes(components)
if not 0 in nodes:
    print('Reference node not found! Ensure that the reference node is labelled as "0"')
    exit()

# get unknown ivs
voltage_sources = get_vs(components)

# get number of unknown nodes, KCL equations, ivs, and voltage sources
len_u_nodes = len(nodes) - 1
len_kcl = len(nodes) - 1
len_ivs = len(voltage_sources)
len_vs = len(voltage_sources)

# generate b matrix, and initialize zero-filled A-matrix
b = np.array([0] * len_kcl + [v.val for v in voltage_sources])
A = np.zeros(((len_u_nodes + len_ivs, len(b))))

# Parse components into A-matrix
height, width = A.shape
time = 1
# Assign KCL equations
for i in range(0, len_kcl):
    row_components = get_neighbour_components(i + 1, components)
    for component in row_components:
        if component.symbol == 'R':
            A[i, i] += 1/component.val
            other_node = component.get_other_node(i + 1)
            if other_node != 0:
                A[i, other_node - 1] += -1/component.val
        elif component.symbol == 'V':
            A[i, len_u_nodes + component.id - 1] += component.get_dir(i + 1)
        elif component.symbol == 'I':
            b[i] += -1 * component.val * component.get_dir(i + 1)
        elif component.symbol == 'C':
            A[i, i] += component.val * time
            other_node = component.get_other_node(i + 1)
            if other_node != 0:
                A[i, other_node - 1] += -1 * component.val * time
                
# Assign voltage equations
for i in range(len_kcl, len_kcl + len_vs):
    if voltage_sources[i - len_kcl].start_node != 0:
        A[i, voltage_sources[i - len_kcl].start_node - 1] = 1
    if voltage_sources[i - len_kcl].end_node != 0:
        A[i, voltage_sources[i - len_kcl].end_node - 1] = -1

# cupy_A = cp_sparse.csr_matrix(csr_matrix(A))
# cupy_b = cp.asarray(b)
# print(type(cupy_A), type(cupy_b))
# cupy_x = cp_sparse.linalg.lsqr(cupy_A, cupy_b)
# x = cp.asnumpy(cupy_x[0])
A_gpu = cp.array(A)
b_gpu = cp.array(b)
x_gpu = cp.linalg.solve(A_gpu, b_gpu)

# x = linalg.lsqr(csr_matrix(A), b)

print('-' * A.shape[0], '\n', A, '\n', '-' * A.shape[0])
print(x_gpu.get())
print(b)
