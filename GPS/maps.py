coord = []
      hfile = open("data.txt","r")
      while True:
        line = hfile.readline()
        if not line:
          break
        line = line.strip().split(",")
        coord.append((float(line[0]),float(line[1])))
      hfile.close()
      unpad_nangor = zip(*coord)
      gmap.polygon(*unpad_nangor, color='cornflowerblue', edge_width=10)
      gmap.draw('map.html')