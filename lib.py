import pandas as pd
import numpy as np
from scipy.sparse import dok_matrix
from components import Resistor, Capacitor, VSource, ISource


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
