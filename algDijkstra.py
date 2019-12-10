import networkx as nx
import matplotlib as plt
import random

def dijkstra(G, s):
    neighbours = [s]; result = []; node = 0
    for i in G.nodes:
        result.append([-1, 100000])
    result[s-1] = [s, 0]
    while len(neighbours) != 0:
        min = 100000
        for i in range(len(neighbours)):
            if result[neighbours[i]-1][1] < min:
                min = result[neighbours[i]-1][1]; node = neighbours[i]
        neighbours.remove(node)
        edges = list(G.edges)
        for edge in edges:
            if edge[0] == node and edge[1] != result[node-1][0]:
                if result[edge[1]-1][0] != -1:
                    if result[edge[1]-1][1] > result[node-1][1] + G.edges[edge[0], edge[1]]["weight"]:
                        result[edge[1] - 1][0] = node
                        result[edge[1] - 1][1] = result[node - 1][1] + G.edges[edge[0], edge[1]]["weight"]
                else:
                    neighbours.append(edge[1])
                    result[edge[1]-1][0] = node; result[edge[1]-1][1] = result[node-1][1] + G.edges[edge[0], edge[1]]["weight"]
    return result

G = nx.Graph(); threshold = 10; app = []
for i in range(1, 10):
    G.add_node(i)
for i in range(1, 10):
    for j in range(1, 10):
        if i != j:
            G.add_edge(i, j, weight = random.randint(1, 20))
result = dijkstra(G, 1)
print(result)
for i in range(len(result)):
    if result[i][1] < threshold:
        app.append(i+1)
print(app)

print(result)


