class Component:
    def __init__(start_node, end_node, val):
        self.start_node = start_node
        self.end_node = end_node
        self.val = val
    
class Resistor(Component):
    self.type = 'passive'

class Capacitor(Component):
    self.type = 'passive'

class VSource(Component):
    self.type = 'active'

class ISource(Component):
    self.type = 'active'