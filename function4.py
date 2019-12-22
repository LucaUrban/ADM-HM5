#%% libraries:
import pandas as pd
import math
import networkx as nx

#%% Reading data:

coordinate = pd.read_csv(r'data/coordinate.txt',header = None, delimiter = ' ')
coordinate.columns = ['v','Id_Node', 'Latitude', 'Longitude']
coordinate.drop('v', axis = 1, inplace = True)

distance = pd.read_csv(r'data/distance.txt',header = None, delimiter = ' ')
distance.columns = ['a', 'Id_Node1', 'Id_Node2', 'd']
distance.drop('a', axis = 1, inplace = True)

time = pd.read_csv(r'data/time.txt',header = None , delimiter = ' ')
time.columns = ['a','Id_Node1', 'Id_Node2', 't']
time.drop('a', axis = 1, inplace = True)

#%% defining sub-functions for distance:

# Euclidean distance:
def ED(x,y):
    d = (((x['Latitude']-y['Latitude']) ** 2) + ((x['Longitude']-y['Longitude']) ** 2)) ** 0.5
    #d = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    return d

# finding successors:
def SCS_dist(close_l, coordinate, distance):
    
    df = distance.loc[distance['Id_Node1'] == close_l[-1]]
    df1 = coordinate.loc[coordinate['Id_Node'].isin(df['Id_Node2'])]
    df1 = df1.reset_index(drop=True)
    
    return df1

# calculating g, h and f scores for distance:
def score_dist(p, y, close_l, g, coordinate, distance):
    # i : Id_Node
    dist = distance.loc[(distance['Id_Node1'] == close_l[-1]) & (distance['Id_Node2'] == p)]
    dist = dist.reset_index(drop=True)
    g1 = g + dist.at[0,'d']
    
    #estimating distance from current node to end node
    h = ED(coordinate.loc[coordinate['Id_Node'] == p], y)
    
    f = g1 + h 
    
    return [g1, h, f]

#%% defining sub-functions for time:
    
# estimating time:
def TM(x, y, coordinate, distance, time):

    # square:
     c = [math.floor((x['Latitude'] + y['Latitude'])/2), math.floor((x['Longitude'] + y['Longitude'])/2)] #center
     r = math.floor(ED(x,y))  #radius
 
     # select nodes in the square:
     df_c = coordinate.loc[(coordinate['Longitude'].isin(range(c[1]-r, c[1]+r))) 
                         & (coordinate['Latitude'].isin(range(c[0]-r, c[0]+r)))]
     
     # filter distance and time of selected nodes: 
     df_d = distance.loc[distance['Id_Node2'].isin(df_c['Id_Node'])]
     df_t = time.loc[time['Id_Node2'].isin(df_c['Id_Node'])]
     
     # estimate time by calculating avearge speed in the area:
     speed = (df_d['d']/df_t['t']).mean()
     time = round(ED(x,y)/speed)
    
     return time

# finding successors:
def SCS_time(close_l, coordinate, time):
    
    df = time.loc[time['Id_Node1'] == close_l[-1]]
    df1 = coordinate.loc[coordinate['Id_Node'].isin(df['Id_Node2'])]
    df1 = df1.reset_index(drop=True)
    
    return df1

# calculating g, h and f scores for distance:
    
def score_time(p, y, close_l, g, coordinate, time, distance):
# p:current node(Id_Node) ,  y:end node, g:score of previous node(parent node)
    
    t = time.loc[(time['Id_Node1'] == close_l[-1]) & (time['Id_Node2'] == p)]
    t = t.reset_index(drop=True)
    g1 = g + t.at[0,'t']
    
    #estimating distance from current node to end node
    h = TM(coordinate.loc[coordinate['Id_Node'] == p], y, coordinate, distance, time)
    
    f = g1 + h 
    
    return [g1, h, f]

#%% finding path:
def path(close_l, DB):
    cost = 0   
    path = [close_l[-1]]
       
    while path[-1] != x[0]:
        
        # if i == x[0] or i == y[0]:
        #     path.append(i)
        point = DB.loc[DB[0] == path[-1]]
        point = point.reset_index(drop = True)
        path.append(point[4][0])
        cost = cost + point[1][0]
    
    path.reverse() 
    return path, cost

#%%A* algorithm:

# A* algorithm for distance:
def A_dist(x, y, coordinate, distance): 
# x : start point and y : end point
    
    open_l = []
    close_l = []
    # columns: Id_Node, g score, h score, f score, previous node
    DB = pd.DataFrame()
    df = pd.DataFrame()
     
    open_l.append(x[0])
    DB = DB.append([[x[0], 0, ED(x,y), ED(x,y),[]]])
    
    # number of iteration
    itr = 0
    
    # check for infeasible route
    inf = 0
    
    while len(open_l):
                    
    # find node with minimum f score, drop it from open list and add it to close list                
        new_DB = DB.loc[DB[0].isin(open_l)]            
        n = new_DB[3].idxmin()
        close_l.append(DB[0][n])
        open_l.remove(DB[0][n])
    
    # check whether find the end node or not    
        if close_l[-1] == y[0]:
            break
    # find successors of new node that added to close list
        
        df = SCS_dist(close_l, coordinate, distance)
        df = df.reset_index(drop=True)
        
        for i in range(len(df)): 
              p = df["Id_Node"][i]
              Pre_Node = close_l[-1]
              Node = DB.loc[DB[0] == Pre_Node]
              s = score_dist(p, y, close_l, int(Node[1]), coordinate, distance)
             
              if p in DB[0].tolist():
                  exist = DB.loc[DB[0] == p].index[0]
                  if DB[1][exist] > int(s[0]):
                    DB[1][exist] = int(s[0])
                    DB[3][exist] = int(s[2])
    
              else:
                  DB = DB.append([[p, s[0], int(s[1]), int(s[2]), Pre_Node]])
                  open_l.append(p)
                  DB = DB.reset_index(drop=True)
                  
        itr += 1
        if itr >= 1500:
            inf = 1
            break
    
    return close_l, DB, inf


# A* algorithm for time:
    
def A_time(x, y, coordinate, time, distance): 
# x : start point and y : end point
    
    open_l = []
    close_l = []
    # columns: Id_Node, g score, h score, f score, previous node
    DB = pd.DataFrame()
    df = pd.DataFrame()
     
    open_l.append(x[0])
    score = TM(x, y, coordinate, distance, time)
    DB = DB.append([[x[0], 0, score, score,[]]])
    
    # number of iteration
    itr = 0
    
    # check for infeasible route
    inf = 0
    
    while len(open_l):
                    
    # find node with minimum f score, drop it from open list and add it to close list                
        new_DB = DB.loc[DB[0].isin(open_l)]            
        n = new_DB[3].idxmin()
        close_l.append(DB[0][n])
        open_l.remove(DB[0][n])
    
    # check whether find the end node or not    
        if close_l[-1] == y[0]:
            break
    # find successors of new node that added to close list
        
        df = SCS_time(close_l, coordinate, time)
        df = df.reset_index(drop=True)
        
        for i in range(len(df)): 
            
              p = df["Id_Node"][i]
              Pre_Node = close_l[-1]
              Node = DB.loc[DB[0] == Pre_Node]
              s = score_time(p, y, close_l, int(Node[1]), coordinate, time, distance)
              if p == y[0]:
                  s[1] = 0
                  s[2] = s[1]
              if p in DB[0].tolist():
                  exist = DB.loc[DB[0] == p].index[0]
                  if DB[1][exist] > int(s[0]):
                    DB[1][exist] = int(s[0])
                    DB[3][exist] = int(s[2])
    
              else:
                  DB = DB.append([[p, s[0], int(s[1]), int(s[2]), Pre_Node]])
                  open_l.append(p)
                  DB = DB.reset_index(drop=True)
                  
        itr += 1
        if itr >= 1500:
            inf = 1
            break
    
    return close_l, DB, inf

#%% Functionality 4 - Shortest Route 

#inputs: 
a = int(input("please enter start node:"))

b = input("please enter a set of nodes that want to path from start node:")
c = [int(i) for i in list(b.split(","))]

d = input("if you want to find path based on distance enter '1', otherwise enter '2':")

# search shortest path:
current_node = a-1
route = []
m = 0
feasible = True

while len(c):
        
    r = []
    ct = 10 ** 20
    
    for i in c:
        
        if d == '1':
            x, y, z = A_dist(coordinate.iloc[current_node], coordinate.iloc[i-1], coordinate, distance)
        else:
            x, y, z = A_time(coordinate.iloc[current_node], coordinate.iloc[i-1], coordinate, time, distance)
        
        if x[-1]  == i:
            p, cost = path(x, y)
            
            check =  any(item in c for item in p[:-1])
            
            if check :
                continue
            elif cost < ct:
                ct = cost
                r = p
            
        elif x[-1] != i  or z == 1:
            feasible = False
            break

    if feasible == False:
        break
       
    route = route + r
    m = m + ct
    current_node = r[-1]-1
    c.remove(r[-1])    

if feasible :
    print(route,m)
else:
    print("Not possible!")


#%% Visualization 4 - Visualize the Shortest Route 

if feasible :
    edges = []

    G=nx.Graph(name="Shoretst path")
    
    route_edges = [(route[n],route[n+1]) for n in range(len(route)-1)]
    G.add_nodes_from(route)
    G.add_edges_from(route_edges)
    edges.append(route_edges)
    
    pos = {}
    for i in route:
        point = coordinate.loc[coordinate['Id_Node'] == i]
        point = point.reset_index(drop=True)
        pos[i] = (point.at[0,'Latitude'], point.at[0,'Longitude'])
    
    nx.draw_networkx_nodes(G,pos=pos)
    nx.draw_networkx_labels(G,pos=pos,font_size = 8)

    for ctr, edgelist in enumerate(edges):
        nx.draw_networkx_edges(G, pos = pos, edgelist = edgelist,
                            edge_color = 'purple', width = [2])

    




    