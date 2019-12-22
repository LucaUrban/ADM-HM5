# importing libraries
import numpy as np
import networkx as nx

def mst_prim(ds, connNodes, notConnNodes):
    # inizialisation of variables
    edges = [];
    result = []

    # costruction of the result
    for i in range(max(ds["id_n1"])):
        result.append([-1, 1000000000])
    result[connNodes[0] - 1] = [connNodes[0], 0]
    result = np.array(result)

    # initialize of the array that contain the edges
    app = np.array(ds[ds["id_n1"] == connNodes[0]])
    for j in range(app.shape[0]):
        if app[j, 1] in notConnNodes:
            edges.append(app[j])

    # Prim's algoritm
    while len(notConnNodes) != 0 and len(edges) != 0:
        costs = [edge[2] for edge in edges]
        for edge in edges:
            if edge[2] == min(costs):
                node = edge[1]
                elRem = edge
                break
        edges.remove(elRem)
        connNodes.append(node);
        notConnNodes.remove(node)
        app = np.array(ds[ds["id_n1"] == node])
        for j in range(app.shape[0]):
            if app[j, 1] in notConnNodes:
                edges.append(app[j])
        if result[elRem[1] - 1][0] == -1:
            result[elRem[1] - 1][0] = elRem[0];
            result[elRem[1] - 1][1] = elRem[2]
    return result


def function2(nodes, functionDist, ds):
    # inizializing principal variables
    finalRes = []
    connNodes = [nodes[0]];
    notConnNodes = nodes;
    notConnNodes.remove(nodes[0])

    # construction of the MST with Prim's algorithm
    if functionDist == "meters": edCol = "Red"
    if functionDist == "time": edCol = "Blue"
    if functionDist == "network": edCol = "Darkgreen"

    # construction of the result
    resultDij = mst_prim(ds, connNodes, notConnNodes)
    for node in connNodes + notConnNodes:
        if resultDij[node - 1][0] == -1:
            return "Not Possible"
        else:
            finalRes.append([node, resultDij[node - 1][0]])
    for el in finalRes:
        if el[0] == el[1]:
            finalRes.remove(el)
    result = nx.Graph()
    for edge in finalRes:
        result.add_nodes_from(edge);
        result.add_edge(edge[0], edge[1])

    # showing the result
    for edge in result.edges:
        print(edge)
    pos = nx.spring_layout(result)
    nx.draw_networkx_nodes(result, pos, node_color="cyan")
    nx.draw_networkx_edges(result, pos, edge_color=edCol)
    nx.draw_networkx_labels(result, pos)