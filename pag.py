import arcpy

fc = "C:\Users\Wojciech\Desktop\semestr5\pag\pag projekt2\pag_projekt2\BDOT_Torun\L4_1_BDOT10k__OT_SKJZ_L.shp"

# Create a search cursor

cursor = arcpy.da.SearchCursor(fc,["OID@", "SHAPE@"]) 

# Create a list of string fields

points = []
edges=[]
i=0
for row in cursor:
    for part in row[1]:
        if (part[0].X,part[0].Y) not in points:
            points.append((part[0].X,part[0].Y))
        if (part[-1].X,part[-1].Y) not in points:
            points.append((part[-1].X,part[-1].Y))

        id_from = points.index((part[0].X,part[0].Y))
        id_to = points.index((part[-1].X, part[-1].Y))

        edges.append([i,part,id_from,id_to])

        i=i+1
        #print ("{0}, {1}, {2}".format(i,part[0].X,part[0].Y))
        #print ("{0}, {1}, {2}".format(i,part[-1].X,part[-1].Y))
    #break;
print len(points)
print len(edges)

vertexes = []
i = 0

for point in points:
    vertexes.append([i,point[0],point[1]])
    i = i+1
print vertexes
