import pandas as pd
from numpy.random import gamma
from math import sqrt
from random import randint, choice
from components import Resistor, Capacitor, VSource, ISource


def gen_rand_circuit_file(fname, num_nodes, avg_connectivity):
    symbols = ['C', 'V', 'I', 'R']
    value_scale = 100
    connections = gen_rand_node_connections(num_nodes, avg_connectivity)
    with open(fname, "w+") as fout:
        fout.write('type,value,start_node,end_node\n')
        for connection in connections:
            fout.write('{},{},{},{}\n'.format(choice(symbols), randint(-1*value_scale, 1*value_scale), connection[0], connection[1]))


def gen_rand_node_connections(num_nodes, avg_connectivity):
    num_components = num_nodes * avg_connectivity
    ungrouped_nodes = num_nodes - 1
    group_sizes = []
    while( ungrouped_nodes > 0):
        group_size = int(gamma(sqrt(num_nodes)//1, sqrt(num_nodes)//2))
        if group_size < 1:
            group_size = 1
        if group_size > ungrouped_nodes:
            group_sizes.append(ungrouped_nodes)
            ungrouped_nodes = 0
        else:
            group_sizes.append(group_size)
            ungrouped_nodes -= group_size
    
    start = 1
    connections = []
    for group_size in group_sizes:
        connections.append((randint(0,start - 1),start))
        for i in range(1, group_size - 1):
            connections.append((start + i, start + i + 1))
        connections.append((start + group_size - 1, randint(0,start - 1)))
        start += group_size
    num_connections_placed = num_nodes + len(group_sizes)
    for i in range(num_components - num_connections_placed):
        first_node = randint(0, num_nodes - 1)
        second_node = randint(0, num_nodes - 1)
        while second_node == first_node:
            second_node = randint(0, num_nodes - 1)
        connections.append((first_node, second_node))
    
    return connections


def parse_stamp(df_row):
    if df_row["type"] == "R":
        return Resistor(df_row["start_node"], df_row["end_node"], df_row["value"])
    if df_row["type"] == "C":
        return Capacitor(df_row["start_node"], df_row["end_node"], df_row["value"])
    if df_row["type"] == "V":
        return VSource(df_row["start_node"], df_row["end_node"], df_row["value"])
    if df_row["type"] == "I":
        return ISource(df_row["start_node"], df_row["end_node"], df_row["value"])


def assign_ids(components):
    symbols = set()
    for component in components:
        symbols.add(component.symbol)
    symbols = {key: 0 for key in symbols}
    for component in components:
        symbols[component.symbol] += 1
        component.set_id(symbols[component.symbol])
    return components


def get_components(df):
    components = []
    for index, row in df.iterrows():
        components.append(parse_stamp(row))
        # similar components are numbered 1-n
        components = assign_ids(components)
    return components


def get_nodes(components):
    nodes = set()
    for component in components:
        nodes.add(component.start_node)
        nodes.add(component.end_node)
    res = list(nodes)
    res.sort()

    if not 0 in nodes:
        raise ValueError(
            'Reference node not found! Ensure that the reference node is labelled as "0"'
        )
    return res


def get_vs(components):
    res = []
    for component in components:
        if component.symbol == "V":
            res.append(component)
    return res


def get_neighbour_components(node, components):
    res = []
    for component in components:
        if component.is_node(node):
            res.append(component)
    return res
