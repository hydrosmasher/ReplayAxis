"""Generate the neutral, welded ReplayAxis body surface using marching tetrahedra."""
import base64
from collections import Counter
from pathlib import Path

import numpy as np

# The viewer rig uses x across the shoulders, y down and z toward the face.
parts = [
    ([0, -.413, 0], [.198, .27, .105]),
    ([0, -.208, -.003], [.120, .23, .074]),
    ([0, -.028, -.002], [.157, .158, .080]),
    ([0, -.693, 0], [.054, .114, .053]),
    ([0, -.843, 0], [.083, .112, .089]),
    ([0, -.890, .033], [.062, .071, .059]),
    ([0, -.861, .088], [.020, .035, .027]),
]
for side in (-1, 1):
    parts.extend([
        ([side*.170,-.576,-.005],[.085,.092,.074]),
        ([side*.070,-.489,.031],[.117,.104,.079]),
        ([side*.076,.049,-.025],[.078,.101,.065]),
        ([side*.080,-.834,-.006],[.018,.032,.022]),
        ([side*.240,-.472,0],[.061,.166,.054]),
        ([side*.304,-.295,0],[.035,.088,.036]),
        ([side*.350,-.163,.005],[.038,.146,.035]),
        ([side*.382,-.018,.008],[.027,.079,.035]),
        ([side*.409,-.033,.025],[.015,.042,.016]),
        ([side*.108,.185,0],[.089,.251,.089]),
        ([side*.112,.408,.010],[.056,.112,.059]),
        ([side*.116,.563,-.012],[.058,.173,.058]),
        ([side*.120,.716,-.007],[.036,.115,.039]),
        ([side*.123,.806,.050],[.048,.052,.111]),
    ])

step = .037
low = np.array([-.57,-1.025,-.24])
size = (32, 53, 14)
grid = np.indices(size).reshape(3,-1).T * step + low
field = np.full(len(grid), 1.)
for center, radius in parts:
    radius = np.array(radius)
    relative = (grid - center) / radius
    distance = (np.linalg.norm(relative, axis=1) - 1) * min(radius)
    blend = .035
    h = np.maximum(blend - abs(field - distance), 0) / blend
    field = np.minimum(field, distance) - h*h*blend*.25

corners = np.array([(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)])
tetrahedra = [(0,1,2,6),(0,2,3,6),(0,3,7,6),(0,7,4,6),(0,4,5,6),(0,5,1,6)]
indices = np.indices(tuple(n-1 for n in size)).reshape(3,-1).T
cells = np.ravel_multi_index((indices[:,None,:]+corners).transpose(2,0,1),size)
mixed = cells[(field[cells].min(axis=1)<0)&(field[cells].max(axis=1)>=0)]
vertices, triangles, edge_vertices = [], [], {}

def intersect(a, b):
    edge = tuple(sorted((a,b)))
    if edge not in edge_vertices:
        fraction = field[a]/(field[a]-field[b])
        edge_vertices[edge] = len(vertices)
        vertices.append(grid[a]+fraction*(grid[b]-grid[a]))
    return edge_vertices[edge]

def add_face(face, outward):
    a,b,c = (vertices[i] for i in face)
    triangles.append(face if np.dot(np.cross(b-a,c-a),outward)>0 else face[::-1])

for cube in mixed:
    for tetra in tetrahedra:
        ids = cube[list(tetra)]
        inside, outside = ids[field[ids]<0], ids[field[ids]>=0]
        if not len(inside) or not len(outside):
            continue
        outward = grid[outside].mean(axis=0)-grid[inside].mean(axis=0)
        if min(len(inside),len(outside)) == 1:
            add_face([intersect(a,b) for a in inside for b in outside],outward)
        else:
            a,b,c,d = [intersect(i,j) for i in inside for j in outside]
            add_face([a,b,c],outward)
            add_face([b,d,c],outward)

edges = Counter(tuple(sorted((f[i],f[(i+1)%3]))) for f in triangles for i in range(3))
assert set(edges.values()) == {2}
adjacent = [set() for _ in vertices]
for a,b in edges:
    adjacent[a].add(b)
    adjacent[b].add(a)
visited = {0}
pending = [0]
while pending:
    neighbors = adjacent[pending.pop()] - visited
    visited.update(neighbors)
    pending.extend(neighbors)
assert len(visited) == len(vertices)
# Smooth grid-induced facets while limiting shrinkage across narrow joints.
vertices = np.array(vertices)
for factor in (.42, -.44, .42, -.44):
    average = np.array([vertices[sorted(neighbors)].mean(axis=0) for neighbors in adjacent])
    vertices += factor * (average - vertices)
data = np.rint(vertices*10000).astype('<i2').tobytes()
faces = np.array(triangles,dtype='<u2').tobytes()
Path('body_mesh.js').write_text(
    f"const neutralVertexData='{base64.b64encode(data).decode()}';\n"
    f"const neutralFaceData='{base64.b64encode(faces).decode()}';\n")
print(f'{len(vertices)} welded vertices, {len(triangles)} faces, one closed surface')
