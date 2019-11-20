import pandas as pd
from math import sqrt
from os import listdir
from lib import gen_rand_circuit_file

for i in range(4, 14):
    gen_rand_circuit_file('rand_data/rand_{}.csv'.format(i), 2**i, int(sqrt(i)))


for fname in listdir('rand_data'):
    with pd.read_csv(fname) as df:
        x = compute_MNA(df, print_eqs=False)
        with open('rand_data_solns/' + fname, 'w+') as fout:
            print(x, file=fout)
        with open('stats.csv', 'w+') as stats_file:
            print('')
