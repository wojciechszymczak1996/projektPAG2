import arcpy

fc = "C:\Users\S276113.S403-K27\Desktop\pag_projekt2\BDOT_Torun\kuj_pom_miasto\L4_1_BDOT10k__OT_SKJZ_L.shp"

# Create a search cursor

cursor = arcpy.da.SearchCursor(fc,["OID@", "SHAPE@"]) 

# Create a list of string fields

points = set()

for row in cursor:
    for part in row[1]:
        points.add((part[0].X,part[0].Y))
        points.add((part[-1].X,part[-1].Y))
        #print ("{0}, {1}, {2}".format(i,part[0].X,part[0].Y))
        #print ("{0}, {1}, {2}".format(i,part[-1].X,part[-1].Y))
    #break;
print len(points)

vertexes = []
i = 0

for point in points:
    vertexes.append([i,point[0],point[1]])
    i = i+1
print vertexes
