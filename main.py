# importing libraries
import pandas as pd
import networkx as nx

# creation of a pandas dataframe and the graph with nodes coordinates
G = nx.Graph()
fileNodes = open("nodesInformations.co", "r"); latitude = 0; longitude = 0; id = 0; matrix = []
with fileNodes as fInput:
    for row in fInput:
        row = row.split()
        if row[0] == "v":
            id = int(row[1])
            latitude = int(row[3][:len(row[3])-1]) / 10 ** (len(row[3]) - 3)
            longitude = -int(row[2][1:len(row[2])-1]) / 10 ** (len(row[2]) - 5)
            matrix.append([id, latitude, longitude])
            G.add_node(id, latitude = latitude, longitude = longitude)
nodesCoordinates = pd.DataFrame(matrix, columns = ["Id", "Latitude", "Longitude"])
fileNodes.close()

# creation of a pandas dataframe with metrics distances
fileMetricDist = open("distanceMatrixMeters.gr", "r"); matrix = []
with fileMetricDist as fInput:
    for row in fInput:
        row = row.split()
        if row[0] == "a":
            matrix.append([int(row[1]), int(row[2]), int(row[3])])
edgesMetrDist = pd.DataFrame(matrix, columns = ["id_n1", "id_n2", "metric_dist"])
fileMetricDist.close()

# creation of a pandas dataframe with time distances
fileTimeDist = open("distanceMatrixSeconds.gr", "r"); latitude = 0; longitude = 0; id = 0; matrix = []
with fileTimeDist as fInput:
    for row in fInput:
        row = row.split()
        if row[0] == "a":
            matrix.append([int(row[1]), int(row[2]), int(row[3])])
edgesTimeDist = pd.DataFrame(matrix, columns = ["id_n1", "id_n2", "time_dist"])
fileTimeDist.close()
print(edgesTimeDist.head(10))

print(G[100])