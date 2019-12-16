def dijkstraF3(G,s,exit):
    neighbours = np.array([[0, s]]); result = []; edges = np.array(list(G.edges))
    for i in G.nodes:
        result.append([-1, 100000])
    result[s-1] = [s, 0]
    result = np.array(result)
    while len(neighbours) != 0:
        costs = [neighbour[0] for neighbour in neighbours]; cont = 0
        if result[exit-1][0] != -1: return result
        for neighbour in neighbours:
            if neighbour[0] == min(costs):
                node = neighbour[1]
                neighbours = np.delete(neighbours, cont, axis = 0)
            cont += 1
        for edge in edges:
            if edge[0] == node and edge[1] != result[node-1][0]:
                if result[edge[1]-1][0] != -1:
                    if result[edge[1]-1][1] > result[node-1][1] + G.edges[edge[0], edge[1]]["weight"]:
                        result[edge[1]-1][0] = node
                        result[edge[1]-1][1] = result[node - 1][1] + G.edges[edge[0], edge[1]]["weight"]
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
  
def function3(source,nodes,functionDist):
    finalRes = set()
    
    if functionDist == "meters":
        for row in edgesMetrDist.values:
            G.add_edge(row[0], row[1], weight = row[2])
    elif functionDist == "time":
        for row in edgesTimeDist.values:
            G.add_edge(row[0], row[1], weight = row[2])
    elif functionDist == "network":
        for row in edgesMetrDist.values:
            G.add_edge(row[0], row[1], weight = 1)
    
    for i in range(len(nodes)):
        resultDij = dijkstraF3(G, source, nodes[i])
        partRes = set()
        pred=nodes[i]
        while resultDij[pred-1][0]!=source: 
            edge = (resultDij[pred-1][0],pred)
            partRes.add(edge)
            pred=resultDij[pred-1][0]
            if resultDij[pred-1][0] == source: 
                partRes.add((pred,source))
        source = nodes[i]
        finalRes = finalRes.union(partRes)
    
    result = nx.Graph()
    for edge in finalRes:
        result.add_nodes_from(edge); result.add_edge(edge[0], edge[1])
    pos = nx.spring_layout(result)
    nx.draw_networkx_nodes(result, pos, node_color = "cyan")
    nx.draw_networkx_edges(result, pos)
    nx.draw_networkx_labels(result, pos)
    

function3(1,[2589,1808], "meters")
