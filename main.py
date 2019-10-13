import pandas as pd
import numpy as np
from scipy.sparse import linalg, csc_matrix, identity

from lib import parse_stamp, get_nodes

df = pd.read_csv("./data/circuit.csv")

components = []
for index, row in df.iterrows():
    components.append(parse_stamp(row))

nodes = get_nodes(**components)
if not 0 in nodes:
    print('Reference node not found! Ensure that the reference node is labelled as "0"')
    exit()

A = identity(height, format="csc")
b = np.ones(height)
x = linalg.spsolve(A, b)

print(x)
