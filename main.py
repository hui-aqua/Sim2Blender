import xml.etree.ElementTree as ET
import numpy as np

amodel_path = "d:/Sim2Blender/testFile1.amodel"
tree = ET.parse(amodel_path)
root = tree.getroot()

# Step 1: Parse all nodes into a dictionary with their IDs
node_dict = {}
for node in root.findall(".//node"):
    node_id = node.get("id")
    x = float(node.get("x"))
    y = float(node.get("y"))
    z = float(node.get("z"))
    node_dict[node_id] = (x, y, z)

# Step 2: Parse beams, membranes, and trusses
edges = []

def parse_component_edges(tag):
    for elem in root.findall(f".//{tag}"):
        nodes = elem.get("nodes")
        if nodes:
            node_ids = nodes.strip().split()
            if len(node_ids) == 2:
                edges.append(tuple(node_ids))
            elif len(node_ids) > 2:
                for i in range(len(node_ids) - 1):
                    edges.append((node_ids[i], node_ids[i + 1]))

for comp in ["beam", "membrane", "truss"]:
    parse_component_edges(comp)

# Step 3: Convert node dict and edges into mesh format (vertices and edges)
vertex_list = list(node_dict.values())
id_to_index = {node_id: idx for idx, node_id in enumerate(node_dict.keys())}
edge_indices = [(id_to_index[start], id_to_index[end]) for start, end in edges if start in id_to_index and end in id_to_index]

# Step 4: Export as OBJ with lines
output_path_with_edges = "d:/Sim2Blender/aquasim_geometry.obj"
with open(output_path_with_edges, "w") as f:
    # Write vertices
    for v in vertex_list:
        f.write(f"v {v[0]} {v[1]} {v[2]}\n")
    # Write edges as lines
    for e in edge_indices:
        # OBJ is 1-indexed
        f.write(f"l {e[0]+1} {e[1]+1}\n")

print(f"Geometry exported to {output_path_with_edges}")
