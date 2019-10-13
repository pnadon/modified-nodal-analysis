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
    if df_row['type'] == 'VS':
        return VSource(
            df_row['start_node'], 
            df_row['end_node'],
            df_row['value'])
    if df_row['type'] == 'IS':
        return ISource(
            df_row['start_node'], 
            df_row['end_node'],
            df_row['value'])

def get_nodes(*components):
    nodes = set()
    for component in components:
        nodes.add(component.start_node)
        nodes.add(component.end_node)
    return list(nodes).sort()