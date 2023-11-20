import serial
import pynmea2 as nmea
import time
import gmplot
apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(-6.90797266607928, 107.7761143223271, 14, apikey=apikey)


port=serial.Serial("/dev/ttyUSB0", 9600)

try:
 while True:
  try:
   mdata = port.readline().decode().strip()
   #print(mdata)
   if "$GPGGA" in mdata:
      msg = nmea.parse(mdata)
      print(msg.latitude, msg.longitude)
      hfile = open("data.txt","a")
      hfile.write("%s,%s\n" % ( msg.latitude, msg.longitude ))
      time.sleep(3)
      hfile.close()

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

  except serial.SerialException as e:
   print("Device error: {}". format(e))
   break
  except nmea.ParseError as e:
   print("Parse error: {}".format(e))
   break
except (KeyboardInterrupt, SystemExit):
 port.close()
 print("Selesai")