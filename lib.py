import pandas as pd
from components import Resistor, Capacitor, VSource, ISource

def parse_stamp(df_row):
    if df_row['type'] == 'R':
        return Resistor(
            df_row['start_node'], 
            df_row['end_node'],
            df_row['value'])
    if df_row['type'] == 'C':
        return Capacitor(
            df_row['start_node'], 
            df_row['end_node'],
            df_row['value'])
    if df_row['type'] == 'V':
        return VSource(
            df_row['start_node'], 
            df_row['end_node'],
            df_row['value'])
    if df_row['type'] == 'I':
        return ISource(
            df_row['start_node'], 
            df_row['end_node'],
            df_row['value'])

def assign_ids(components):
    symbols = set()
    for component in components:
        symbols.add(component.symbol)
    symbols = {key: 0 for key in symbols}
    for component in components:
        symbols[component.symbol] += 1
        component.set_id(symbols[component.symbol])
    return components
        

def get_nodes(components):
    nodes = set()
    for component in components:
        nodes.add(component.start_node)
        nodes.add(component.end_node)
    res = list(nodes)
    res.sort()
    return res

def get_vs(components):
    res = []
    for component in components:
        if component.symbol == 'V':
            res.append(component)
    return res

def get_neighbour_components(node, components):
    res = []
    for component in components:
        if component.is_node(node):
            res.append(component)
    return res