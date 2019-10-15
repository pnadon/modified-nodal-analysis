class Component:
    def __init__(self, start_node, end_node, val):
        self.symbol = ''
        self.type = 'generic'
        self.start_node = start_node
        self.end_node = end_node
        self.val = val
        self.id = -1

    def is_node(self, node):
        if (self.start_node == node) or (self.end_node == node):
            return True
        else:
            return False

    def set_id(self, id_num):
        self.id = id_num

    def get_dir(self, node):
        if self.start_node == node:
            return 1
        elif self.end_node == node:
            return -1
        else:
            return 'error'

    def get_other_node(self, node):
        if self.start_node != node and self.end_node == node:
            return self.start_node
        elif self.end_node != node and self.start_node == node:
            return self.end_node
        else:
            return -1
    
class Resistor(Component):
    def __init__(self, start_node, end_node, val):
        super().__init__(start_node, end_node, val)
        self.symbol = 'R'
        self.type = 'passive'

class Capacitor(Component):
    def __init__(self, start_node, end_node, val):
        super().__init__(start_node, end_node, val)
        self.symbol = 'C'
        self.type = 'passive'

class VSource(Component):
    def __init__(self, start_node, end_node, val):
        super().__init__(start_node, end_node, val)
        self.symbol = 'V'
        self.type = 'active'

class ISource(Component):
    def __init__(self, start_node, end_node, val):
        super().__init__(start_node, end_node, val)
        self.symbol = 'I'
        self.type = 'active'