# modified-nodal-analysis
 a project for simulating MNA using Julia
[reference](https://lpsa.swarthmore.edu/Systems/Electrical/mna/MNA3.html)

# MNA steps:
1. Select a reference node (usually ground) and name the remaining n-1 nodes.  Also label currents through each current source.  
2. Assign a name to the current through each voltage source.  We will use the convention that the current flows from the positive node to the negative node of the source.
3. Apply Kirchoff's current law to each node.  We will take currents out of the node to be positive.
4. Write an equation for the voltage each voltage source.
5. Solve the system of n-1 unknowns.

# Definitions / rules:
- [node](en.wikipedia.org/wiki/Node_(circuits)): "any point on a circuit where the terminals of two or more circuit elements meet"
- **essential node**: a node with 3+ elements (nodes with 2 elements arent very interesting voltage-wise)
- **reference node** (usually labelled ground): try to choose the one with the most connections
  - when you measure voltage drop / rises, you need to measure them relative to another voltage, which is the voltage at the reference node
- for *n* nodes, you needs *n-1* equations
- writing equations:
  - v = ir
- **KCL**: sum i_{in} = sum i_{out} of a node / sub-circuit, where i = current
- elements in series have identical current
- loop: trajectory that does not cross any node more than once
- **KVL**: the sum of voltage changes in a loop is zero
