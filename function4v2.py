# importing libraries
import numpy as np
import networkx as nx

def dijkstraF4(ds, s, nodes):
    neighbours = [[0, s]];
    result = []
    for i in range(max(ds["id_n1"])):
        result.append([-1, 1000000000])
    result[s - 1] = [s, 0]
    result = np.array(result)
    while len(neighbours) != 0:
        costs = [neighbour[0] for neighbour in neighbours]
        for el in nodes:
            if result[el - 1][0] != -1: return el, result
        for neighbour in neighbours:
            if neighbour[0] == min(costs):
                node = neighbour[1]
                elRem = neighbour
        neighbours.remove(elRem)
        app = np.array(ds[ds["id_n1"] == node])
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


def function4(source, nodes, functionDist, ds):
    # inizialisation of variables and choice of the edges color
    finalRes = set();
    sourceIn = source
    if functionDist == "meters": edCol = "Red"
    if functionDist == "time": edCol = "Blue"
    if functionDist == "network": edCol = "Darkgreen"

    # controlling if it's possible to find a path through the nodes
    for node in nodes:
        if len(ds[ds["id_n2"] == node]) == 0:
            return "Not possible"

    # extracting the result based on subsequent Dijkstra paths
    while len(nodes) != 0:
        if functionDist == "meters": node, resultDij = dijkstraF4(ds, source, nodes)
        if functionDist == "time": node, resultDij = dijkstraF4(ds, source, nodes)
        if functionDist == "network": node, resultDij = dijkstraF4(ds, source, nodes)
        pred = node;
        nodes.remove(node);
        partRes = set()
        while resultDij[pred - 1][0] != source:
            edge = (resultDij[pred - 1][0], pred);
            partRes.add(edge)
            pred = resultDij[pred - 1][0]
            if resultDij[pred - 1][0] == source:
                partRes.add((pred, source))
        source = node;
        finalRes = finalRes.union(partRes)

    # creation of result graph
    result = nx.Graph()
    for edge in finalRes:
        result.add_nodes_from(edge);
        result.add_edge(edge[0], edge[1])

    # vizualization of the result
    colors = [];
    pos = nx.spring_layout(result)
    for node in result.nodes:
        if node == sourceIn:
            colors.append("Red")
        else:
            colors.append("Cyan")
    nx.draw_networkx_nodes(result, pos, node_color=colors)
    nx.draw_networkx_edges(result, pos, edge_color=edCol)
    nx.draw_networkx_labels(result, pos)