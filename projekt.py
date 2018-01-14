import arcpy
import networkx
arcpy.env.overwriteOutput = True

G = networkx.DiGraph()
fc = "C:\Users\Wojciech\Desktop\semestr5\pag\pag projekt2\pag_projekt2\BDOT_Torun\L4_1_BDOT10k__OT_SKJZ_L.shp"
cursor = arcpy.da.SearchCursor(fc,["OID@", "SHAPE@", "SHAPE@LENGTH", "klasaDrogi"])

points = []
edges = []
i=0
for row in cursor:
    for part in row[1]:
        if (part[0].X,part[0].Y) not in points:
            G.add_node(i, X = part[0].X, Y = part[0].Y)
            i = i + 1
            points.append((part[0].X,part[0].Y))
        if (part[-1].X,part[-1].Y) not in points:
            G.add_node(i, X = part[-1].X, Y = part[-1].Y)
            i = i + 1
            points.append((part[-1].X,part[-1].Y))

        id_from = points.index((part[0].X,part[0].Y))
        id_to = points.index((part[-1].X, part[-1].Y))

        if row[3]=='A':
            speed=120
        elif row[3] == 'D' or row[3] =='I' or row[3] =='L' or row[3] =='Z':
            speed = 40
        elif row[3] == 'G':
            speed = 70
        elif row[3] == 'GP':
            speed = 90
        elif row[3] == 'S':
            speed = 110
        time = row[2]/speed/1000*60
        G.add_edge(id_from, id_to, ObjectID = row[0], length = row[2], time = time)
        edges.append([id_from, id_to, row[0], row[2], time])
        if row[0]%5!=0:
            G.add_edge(id_to, id_from, ObjectID = row[0], length = row[2], time = time)
            edges.append([id_to, id_from, row[0], row[2], time])
numOfNodes = networkx.number_of_nodes(G)
numOfEdges = networkx.number_of_edges(G)

with open('edgesNodes.txt','w') as f:
    f.write('EDGES\n')
    f.write('ID, X, Y\n')
    nodes = [None] * networkx.number_of_nodes(G)
    for id, x in networkx.get_node_attributes(G,'X').items():
        nodes[id] = ', '.join([str(id),str(x)])
    for id, y in networkx.get_node_attributes(G,'Y').items():
        nodes[id] = ', '.join([nodes[id],str(x)])
    for node in nodes:
        f.write(node)
        f.write('\n')
    i=0
    f.write('NODES\n')
    f.write('ID_FROM, ID_TO, OBJECT_ID, LENGTH, TIME\n')
    edges = [None] * networkx.number_of_edges(G)
    for ids, oid in networkx.get_edge_attributes(G,'ObjectID').items():
        edges[i] = ', '.join([str(ids[0]),str(ids[1]),str(oid)])
        i = i + 1
    i=0
    for ids, length in networkx.get_edge_attributes(G,'length').items():
        edges[i] = ', '.join([edges[i],str(length)])
        i = i + 1
    i = 0
    for ids, time in networkx.get_edge_attributes(G, 'time').items():
        edges[i] = ', '.join([edges[i], str(time)])
        i = i + 1
    for edge in edges:
        f.write(edge)
        f.write('\n')
features=[]
arcpy.CreateFeatureclass_management("C:\Users\Wojciech\Desktop\semestr5\pag\pag projekt2\wyniki", "points.shp", "POINT")

cursor = arcpy.da.InsertCursor("C:\Users\Wojciech\Desktop\semestr5\pag\pag projekt2\wyniki\points.shp", ("ID", "SHAPE@XY"))
with open('dijkstra.txt', 'w') as f:
    for key, value in networkx.single_source_dijkstra_path_length(G,0,cutoff=3,weight='time').items():

        f.write('FROM 0 TO {0} IS {1} MINUTES\n'.format(key,value))

        X=networkx.get_node_attributes(G,'X')
        X=X[key]
        Y=networkx.get_node_attributes(G,'Y')
        Y=Y[key]
        row = [key,(X,Y)]
        cursor.insertRow(row)
        rest=2-value
        for key in G.in_edges(key, data=True):
            dist = rest/key[2]['time']*100
            length = abs(dist*key[2]['length']/100)
            if dist <100:
                pntGeom = arcpy.PointGeometry(arcpy.Point(X,Y))
                features.append(pntGeom.buffer(length))

del cursor
arcpy.CopyFeatures_management(features, "C:\Users\Wojciech\Desktop\semestr5\pag\pag projekt2\wyniki\okregi.shp")
arcpy.MinimumBoundingGeometry_management("C:\Users\Wojciech\Desktop\semestr5\pag\pag projekt2\wyniki\points.shp",
                                         "C:\Users\Wojciech\Desktop\semestr5\pag\pag projekt2\wyniki\convex_points.shp",
                                         "CONVEX_HULL", "ALL")
