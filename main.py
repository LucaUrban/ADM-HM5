# importing libraries
import pandas as pd
import function1 as f1
import function2 as f2
import function3 as f3
import function4 as f4

# creation of a pandas dataframe with nodes coordinates
fileNodes = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\ADM-HM5\\nodesInformations.co", "r")
latitude = 0; longitude = 0; id = 0; matrix = []
with fileNodes as fInput:
    for row in fInput:
        row = row.split()
        if row[0] == "v":
            id = int(row[1])
            latitude = int(row[3][:len(row[3])-1]) / 10 ** (len(row[3]) - 3)
            longitude = -int(row[2][1:len(row[2])-1]) / 10 ** (len(row[2]) - 5)
            matrix.append([id, latitude, longitude])
nodesCoordinates = pd.DataFrame(matrix, columns = ["Id", "Latitude", "Longitude"])
fileNodes.close()

# creation of a pandas dataframe with metrics distances
fileMetricDist = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\ADM-HM5\\distanceMatrixMeters.gr", "r")
matrix = []
with fileMetricDist as fInput:
    for row in fInput:
        row = row.split()
        if row[0] == "a":
            matrix.append([int(row[1]), int(row[2]), int(row[3])])
edgesMetrDist = pd.DataFrame(matrix, columns = ["id_n1", "id_n2", "metric_dist"])
fileMetricDist.close()

# creation of a pandas dataframe with time distances
fileTimeDist = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\ADM-HM5\\distanceMatrixSeconds.gr", "r")
matrix = []
with fileTimeDist as fInput:
    for row in fInput:
        row = row.split()
        if row[0] == "a":
            matrix.append([int(row[1]), int(row[2]), int(row[3])])
edgesTimeDist = pd.DataFrame(matrix, columns = ["id_n1", "id_n2", "time_dist"])
matrix = []

# creation of a pandas dataframe with network distances
fileTimeDist = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\ADM-HM5\\distanceMatrixSeconds.gr", "r")
matrix = []
with fileTimeDist as fInput:
    for row in fInput:
        row = row.split()
        if row[0] == "a":
            matrix.append([int(row[1]), int(row[2]), 1])
edgesNetDist = pd.DataFrame(matrix, columns = ["id_n1", "id_n2", "network_dist"])
fileTimeDist.close(); matrix = []

# choice of the function (made by the user)
choice = 0
while choice != -1:
    choice = input("Insert the number of the function that you want to use (from 1 to 4, -1 to exit). \n1 to find the neighbours in a limited distance\n2 to find the smartest network\n3 to find the shortest path into an ordered list of waypoints\n4 to find the path into a set of waypoints\n")
    while int(choice) not in [-1, 1, 2, 3, 4]:
            choice = input("Insert the number of the function that you want to use (from 1 to 4, -1 to exit). \n1 to find the neighbours in a limited distance\n2 to find the smartest network\n3 to find the shortest path into an ordered list of waypoints\n4 to find the path into a set of waypoints\n")
    if int(choice) == 1:
        source = input("Insert the node where you want to start: ")
        functionDist = input("Insert the type of distances (meters for metric distance, time for time distance or network for network distance): ")
        threshold = input("Insert the threshold: ")
        if functionDist == "meters": f1.function1(int(source), functionDist, int(threshold), edgesMetrDist)
        if functionDist == "time": f1.function1(int(source), functionDist, int(threshold), edgesTimeDist)
        if functionDist == "network": f1.function1(int(source), functionDist, int(threshold), edgesNetDist)
    if int(choice) == 2:
        nodes = input("Insert the nodes that you want to include into your walk (divided by a space): ")
        functionDist = input("Insert the type of distances (meters for metric distance, time for time distance or network for network distance): ")
        if functionDist == "meters": f2.function2(list(map(int, nodes.split(" "))), functionDist, edgesMetrDist)
        if functionDist == "time": f2.function2(list(map(int, nodes.split(" "))), functionDist, edgesTimeDist)
        if functionDist == "network": f2.function2(list(map(int, nodes.split(" "))), functionDist, edgesNetDist)
    if int(choice) == 3:
        source = input("Insert the node where you want to start: ")
        nodes = input("Insert the nodes that you want to include into your walk (divided by a space): ")
        functionDist = input("Insert the type of distances (meters for metric distance, time for time distance or network for network distance): ")
        if functionDist == "meters": f3.function3(int(source), list(map(int, nodes.split(" "))), functionDist, edgesMetrDist)
        if functionDist == "time": f3.function3(int(source), list(map(int, nodes.split(" "))), functionDist, edgesTimeDist)
        if functionDist == "network": f3.function3(int(source), list(map(int, nodes.split(" "))), functionDist, edgesNetDist)
    if int(choice) == 4:
        source = input("Insert the number of node that represent the node where you want to start: ")
        nodes = input("Insert the nodes that you want to include into your walk (divided by a space): ")
        functionDist = input("Insert the type of distances (meters for metric distance, time for time distance or network for network distance): ")
        if functionDist == "meters": f4.function4(int(source), list(map(int, nodes.split(" "))), functionDist, edgesMetrDist)
        if functionDist == "time": f4.function4(int(source), list(map(int, nodes.split(" "))), functionDist, edgesTimeDist)
        if functionDist == "network": f4.function4(int(source), list(map(int, nodes.split(" "))), functionDist, edgesNetDist)
    if int(choice) == -1: break