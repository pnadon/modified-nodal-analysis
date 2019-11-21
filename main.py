import pandas as pd
from math import sqrt
from os import listdir
from lib import gen_rand_circuit_file
from mna_solver import benchmark_MNA

with open("stats.csv", "w+") as stats_file:
    print(
        "fname,matrix_size,num_nodes,avg_connectivity,num_components,processor,total,transfer,solve",
        file=stats_file,
    )

for avg_connectivity in range(2, 6):
    for j in range(3, 25):
        fname = "rand_data/rand_size-{:03}_density-{:03}.csv".format(j,avg_connectivity)
        num_nodes = int(sqrt(2 ** j))
        gen_rand_circuit_file(fname, num_nodes, avg_connectivity)
        df = pd.read_csv(fname)
        benchmark = benchmark_MNA(df)
        with open("stats.csv", "a+") as stats_file:
            print(
                "{},{},{},{},{},{},{},{},{}".format(
                    fname,
                    benchmark["matrix_size"][0],
                    num_nodes,
                    avg_connectivity,
                    benchmark["num_components"],
                    'cuda',
                    benchmark["cuda"]["total"],
                    benchmark["cuda"]["data transfer"],
                    benchmark["cuda"]["linear solve"],
                ),
                file=stats_file,
            )
            print(
                "{},{},{},{},{},{},{},{},{}".format(
                    fname,
                    benchmark["matrix_size"][0],
                    num_nodes,
                    avg_connectivity,
                    benchmark["num_components"],
                    'cpu',
                    benchmark["cpu"]["total"],
                    benchmark["cpu"]["data transfer"],
                    benchmark["cpu"]["linear solve"],
                ),
                file=stats_file,
            )
    
