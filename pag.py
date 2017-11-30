import arcpy
import networkx

# https://networkx.github.io/documentation/networkx-1.10/reference/index.html
G = networkx.Graph()

fc = "C:\Users\S276113.S403-K27\Desktop\pag_projekt2\BDOT_Torun\kuj_pom_miasto\L4_1_BDOT10k__OT_SKJZ_L.shp"
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
    break;
print len(points)
print networkx.number_of_nodes(G)
print len(edges)
print networkx.number_of_edges(G)

print networkx.get_node_attributes(G,['X','Y'])
