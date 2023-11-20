import gmplot
apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(-6.90797266607928, 107.7761143223271, 14, apikey=apikey)

def myMap():
  coord = []
  hfile = open('data.txt',"r")
  while True:
    line = hfile.readline()
    if not line:
        break
    line = line.strip().split(",")
    coord.append((float(line[0]),float(line[1])))
  hfile.close()
  unpad_nangor = zip(*coord)
  route = zip(*coord)
  gmap.polygon(*unpad_nangor, color='red', edge_width=10,face_alpha = 0)

  coord = []
  hfile = open('data.txt',"r")
  while True:
    line = hfile.readline()
    if not line:
        break
    line = line.strip().split(",")
    coord.append((float(line[0]),float(line[1])))
  hfile.close()
  unpad_nangor = zip(*coord)
  gmap.polygon(*unpad_nangor, color='blue', edge_width=1, face_alpha = 0,)
  gmap.draw('C:/Users/Lenovo/PycharmProjects/pythonProject/map.html')
myMap()