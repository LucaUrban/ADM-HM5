# importing libraries
import numpy as np
import networkx as nx

# The dijkstra algoritm for the first function
def dijkstraF1(ds, s, threshold):
    # initialisation of variables
    neighbours = [[0, s]]; result = []

    # construction of result array
    for i in range(max(ds["id_n1"])):
        result.append([-1, 1000000000])
    result[s - 1] = [s, 0]
    result = np.array(result)

    # main part of Dijkstra algorithm
    while len(neighbours) != 0:
        # extraction of the minimum and removing of that element
        costs = [neighbour[0] for neighbour in neighbours]
        if min(costs) > threshold: return result
        for neighbour in neighbours:
            if neighbour[0] == min(costs):
                node = neighbour[1]
                elRem = neighbour
        neighbours.remove(elRem)
        app = np.array(ds[ds["id_n1"] == node])

        # update of paths
        for j in range(app.shape[0]):
            if app[j, 1] != result[node - 1][0]:
                if result[app[j, 1] - 1][0] != -1:
                    if result[app[j, 1] - 1][1] > result[node - 1][1] + app[j, 2]:
                        result[app[j, 1] - 1][0] = node
                        result[app[j, 1] - 1][1] = result[node - 1][1] + app[j, 2]
                else:
                    neighbours.append([result[node - 1][1] + app[j, 2], app[j, 1]])
                    result[app[j, 1] - 1][0] = node
                    result[app[j, 1] - 1][1] = result[node - 1][1] + app[j, 2]
    return result


def function1(source, functionDist, threshold, ds):
    finalRes = []

    # choising edges colors basing on the distance function
    if functionDist == "meters": edCol = "Red"
    if functionDist == "time": edCol = "Blue"
    if functionDist == "network": edCol = "Darkgreen"

    # construction of the result
    resultDij = dijkstraF1(ds, source, threshold)
    for i in range(len(resultDij)):
        if resultDij[i][1] < threshold:
            finalRes.append([i + 1, resultDij[i][0]])

    # costruction of the result graph
    result = nx.Graph()
    for i in range(len(finalRes)):
        result.add_node(finalRes[i][0])
        result.add_edge(finalRes[i][0], finalRes[i][1])

    # vizualization of the result
    colors = []; pos = nx.spring_layout(result)
    for node in result.nodes:
        if node == source:
            colors.append("Red")
        else:
            colors.append("Cyan")
    nx.draw_networkx_nodes(result, pos, node_color=colors)
    nx.draw_networkx_edges(result, pos, edge_color=edCol)
    nx.draw_networkx_labels(result, pos)