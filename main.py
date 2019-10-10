import pandas as pd
import numpy as np
from scipy.sparse import linalg, csc_matrix, identity

df = pd.read_csv('./data/circuit.csv')

height = 10

A = identity(height, format="csc")
b = np.ones(height,)
x = linalg.spsolve(A, b)

print(x)
