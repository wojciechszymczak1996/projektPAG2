import arcpy
import networkx

'''
https://networkx.github.io/documentation/networkx-1.10/reference/index.html
https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.classes.function.all_neighbors.html
https://community.esri.com/thread/87205
http://pro.arcgis.com/en/pro-app/tool-reference/data-management/minimum-bounding-geometry.htm
'''
G = networkx.Graph()

fc = "C:\Users\Rodzice\Desktop\Geoinformatyka\PAG2\cwiczenia\projekt2\kujawsko_pomorskie_m_Torun\L4_1_BDOT10k__OT_SKJZ_L.shp"
cursor = arcpy.da.SearchCursor(fc,["OID@", "SHAPE@", "SHAPE@LENGTH"]) 

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

        G.add_edge(id_from, id_to, ObjectID = row[0], length = row[2])
        edges.append([id_from, id_to, row[0], row[2]])
numOfNodes = networkx.number_of_nodes(G)
numOfEdges = networkx.number_of_edges(G)

print numOfNodes
print numOfEdges

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
    f.write('ID_FROM, ID_TO, OBJECT_ID, LENGTH\n')
    edges = [None] * networkx.number_of_edges(G)
    for ids, oid in networkx.get_edge_attributes(G,'ObjectID').items():
        edges[i] = ', '.join([str(ids[0]),str(ids[1]),str(oid)])
        i = i + 1
    i=0
    for ids, length in networkx.get_edge_attributes(G,'length').items():
        edges[i] = ', '.join([edges[i],str(length)])
        i = i + 1
    for edge in edges:
        f.write(edge)
        f.write('\n')

with open('dijkstra.txt','w') as f:
    for key, value in networkx.single_source_dijkstra_path_length(G,0,cutoff=1000,weight='length').items():
        if key == 0:
            continue;
        f.write('FROM 0 TO {0} IS {1} METERS\n'.format(key,value))
