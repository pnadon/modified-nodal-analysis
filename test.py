import cupy as cp
import cupyx.scipy.sparse as cp_sparse
from scipy.sparse import dok_matrix
from numpy import zeros

def construct_3d_matrix(m_height, m_width):
    """constructs the A matrix for the 3D network

    :param pmap: the mapper class for the 3D network
    :param eqns: the equation class for the 3D network
    :return: the constructed A matrix
    """
    a = dok_matrix((m_height, m_width))

    for i in range(m_height):
        a[i,i] = 1
    return a

def construct_b(start_vals, end_vals, length, count, num_vars):
    ordered_start_vals = [k for k in sorted(start_vals)]
    ordered_end_vals = [k for k in sorted(end_vals)]
    b = zeros((length,))
    for i in range(count):
        for val in range(num_vars):
            b[val + i * num_vars] = ordered_start_vals[val]
            b[val - (i + 1) * num_vars] = ordered_end_vals[val]
    return b

def solve_3d_equilibrium_lsqr_gpu(m_width, size_dirichlet_face, num_vars, start_vals, end_vals):
    cupy_A = cp_sparse.csr_matrix(construct_3d_matrix(m_width, m_width))
    cupy_b = cp.asarray(construct_b(start_vals, end_vals, m_width, size_dirichlet_face, num_vars))
    cupy_x = cp_sparse.linalg.lsqr(cupy_A, cupy_b)
    x = cp.asnumpy(cupy_x[0])

    print('---' * m_width, '\n', cupy_A.get(), '\n', '---' * m_width)
    print(cupy_x)
    print(cupy_b.get())

solve_3d_equilibrium_lsqr_gpu(20, 4, 2, (1, 2), (3,4))