# modified-nodal-analysis
 a project for simulating MNA using Julia

# MNA steps:
1. Select a reference node (usually ground) and name the remaining n-1 nodes.  Also label currents through each current source.  
2. Assign a name to the current through each voltage source.  We will use the convention that the current flows from the positive node to the negative node of the source.
3. Apply Kirchoff's current law to each node.  We will take currents out of the node to be positive.
4. Write an equation for the voltage each voltage source.
5. Solve the system of n-1 unknowns.

# Definitions:
[node](en.wikipedia.org/wiki/Node_(circuits)): "any point on a circuit where the terminals of two or more circuit elements meet"
