# from "python -m pip install cupy" -- MUST HAVE CUDA SETUP
from scipy.sparse import dok_matrix, csr_matrix
from scipy.sparse.linalg import lsqr
import numpy as np
import cupy as cp
import cupyx.scipy.sparse as cp_sparse
from timeit import default_timer as timer
from lib import (
    get_nodes,
    get_vs,
    get_neighbour_components,
    get_components,
)


def benchmark_MNA(df):
    components = get_components(df)
    nodes = get_nodes(components)

    # get unknown ivs
    voltage_sources = get_vs(components)
    num_nodes = len(nodes)

    # generate b matrix, and initialize zero-filled A-matrix
    b = construct_b(voltage_sources, num_nodes)
    A = construct_A(b, components, voltage_sources, num_nodes)

    start_cuda = timer()
    mid_cuda = -1
    try:
        cupy_A = cp_sparse.csr_matrix(A)
        cupy_b = cp.asarray(b)
        mid_cuda = timer()
        cupy_x = cp_sparse.linalg.lsqr(cupy_A, cupy_b)[0]
    except:
        print('failed to solve on gpu')
        mid_cuda = -1
    end_cuda = timer()

    start_cpu = timer()
    A = csr_matrix(A)
    mid_cpu = timer()
    x = lsqr(A, b)
    end_cpu = timer()

    if mid_cuda == -1:
        cuda_trans_diff = ""
        cuda_solve_diff = ""
    else:
        cuda_trans_diff = mid_cuda - start_cuda
        cuda_solve_diff = end_cuda - mid_cuda
    return {
        'matrix_size': A.shape,
        'num_components': len(components),
        'cpu': {
            'total': end_cpu - start_cpu,
            'data transfer': mid_cpu - start_cpu,
            'linear solve': end_cpu - mid_cpu
        },
        'cuda': {
            'total': end_cuda - start_cuda,
            'data transfer': cuda_trans_diff,
            'linear solve': cuda_solve_diff
        }
    }


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


def construct_A(b, components, voltage_sources, num_nodes):
    len_u_nodes = num_nodes - 1
    len_kcl = num_nodes - 1
    len_ivs = len(voltage_sources)
    len_vs = len(voltage_sources)
    A = dok_matrix((len_u_nodes + len_ivs, len(b)))

    # Parse components into A-matrix
    height, width = A.shape
    time = 1
    # Assign KCL equations
    for i in range(0, len_kcl):
        row_components = get_neighbour_components(i + 1, components)
        for component in row_components:
            if component.symbol == "R":
                A[i, i] += 1 / component.val
                other_node = component.get_other_node(i + 1)
                if other_node != 0:
                    A[i, other_node - 1] += -1 / component.val
            elif component.symbol == "V":
                A[i, len_u_nodes + component.id - 1] += component.get_dir(i + 1)
            elif component.symbol == "I":
                b[i] += -1 * component.val * component.get_dir(i + 1)
            elif component.symbol == "C":
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

    return A


def construct_b(voltage_sources, num_nodes):
    len_kcl = num_nodes - 1
    len_b = len_kcl + len(voltage_sources)
    b = np.zeros((len_b,))
    for i in range(len_kcl, len_b):
        b[i] = voltage_sources[i - len_kcl].val
    return b