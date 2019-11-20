import pandas as pd
from math import sqrt
from os import listdir
from lib import gen_rand_circuit_file
from mna_solver import benchmark_MNA

for i in range(3, 25):
    gen_rand_circuit_file("rand_data/rand_{:03}.csv".format(i), int(sqrt(2 ** i)), 3)

with open("stats.csv", "w+") as stats_file:
    print(
        "fname,matrix_size,num_components,processor,total,transfer,solve",
        file=stats_file,
    )
for fname in listdir("rand_data"):
    df = pd.read_csv("rand_data/" + fname)
    benchmark = benchmark_MNA(df)
    with open("stats.csv", "a+") as stats_file:
        print(
            "{},{},{},{},{},{},{}".format(
                fname,
                benchmark["matrix_size"][0],
                benchmark["num_components"],
                'cuda',
                benchmark["cuda"]["total"],
                benchmark["cuda"]["data transfer"],
                benchmark["cuda"]["linear solve"],
            ),
            file=stats_file,
        )
        print(
            "{},{},{},{},{},{},{}".format(
                fname,
                benchmark["matrix_size"][0],
                benchmark["num_components"],
                'cpu',
                benchmark["cpu"]["total"],
                benchmark["cpu"]["data transfer"],
                benchmark["cpu"]["linear solve"],
            ),
            file=stats_file,
        )
