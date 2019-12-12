import networkx as nx
import random
import numpy as np
import queue

class nodePriority:
    def __init__(self, priority, node):
        self.priority = priority
        self.node = node

    def __lt__(self, other):
        return self.priority > other.priority

def dijkstra(G, s, threshold):
    neighbours = np.array([[0, s]]); result = []; edges = np.array(list(G.edges))
    for i in G.nodes:
        result.append([-1, 100000])
    result[s-1] = [s, 0]
    result = np.array(result)
    while len(neighbours) != 0:
        costs = [neighbour[0] for neighbour in neighbours]; cont = 0
        if min(costs) > threshold:
            return result
        for neighbour in neighbours:
            if neighbour[0] == min(costs):
                node = neighbour[1]
                neighbours = np.delete(neighbours, cont, axis = 0)
            cont += 1
        for edge in edges:
            if edge[0] == node and edge[1] != result[node-1][0]:
                if result[edge[1]-1][0] != -1:
                    if result[edge[1]-1][1] > result[node-1][1] + G.edges[edge[0], edge[1]]["weight"]:
                        result[edge[1] - 1][0] = node
                        result[edge[1] - 1][1] = result[node - 1][1] + G.edges[edge[0], edge[1]]["weight"]
                else:
                    neighbours = np.append(neighbours, [[result[node-1][1] + G.edges[edge[0], edge[1]]["weight"], edge[1]]], axis = 0)
                    result[edge[1]-1][0] = node
                    result[edge[1]-1][1] = result[node-1][1] + G.edges[edge[0], edge[1]]["weight"]
            if edge[1] == node and edge[0] != result[edge[1]-1][0]:
                if result[edge[0]-1][0] != -1:
                    if result[edge[0]-1][1] > result[edge[1]-1][1] + G.edges[edge[0], edge[1]]["weight"]:
                        result[edge[0] - 1][0] = node
                        result[edge[0] - 1][1] = result[edge[1] - 1][1] + G.edges[edge[0], edge[1]]["weight"]
                else:
                    neighbours = np.append(neighbours, [[result[edge[1]-1][1] + G.edges[edge[0], edge[1]]["weight"], edge[0]]], axis = 0)
                    result[edge[0]-1][0] = edge[1]
                    result[edge[0]-1][1] = result[edge[1]-1][1] + G.edges[edge[0], edge[1]]["weight"]
    return result

G = nx.Graph(); threshold = 10; app = []
for i in range(1, 10):
    G.add_node(i)
for i in range(1, 10):
    for j in range(1, 10):
        num = random.randint(0, 10)
        if num > 6 and i != j:
            G.add_edge(i, j, weight = random.randint(1, 20))
print(G.edges)
print([G.edges[edge] for edge in G.edges])
resultDij = dijkstra(G, 1, 10)
for i in range(len(resultDij)):
    if resultDij[i][1] < threshold:
        app.append([i+1, resultDij[i][0]])
result = nx.Graph()
for i in range(len(app)):
    result.add_node(app[i][0])
    if i > 0: result.add_edge(app[i][0], app[i][1])
print(resultDij)