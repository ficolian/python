import math
from math import *
import RPi.GPIO as GPIO
import threading
import serial
import pynmea2 as nmea
import time
import gmplot
from i2clibraries import i2c_hmc5883l
import time
# import geopy.distance

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)  # Steer Right
GPIO.setup(20,GPIO.OUT)  # Steer Left
GPIO.setup(16,GPIO.OUT)  # Control
GPIO.setup(6,GPIO.OUT)   # Move Forward
# GPIO.setup(26,GPIO.OUT)  # Move Backward
# GPIO.setup(12,GPIO.OUT)  # Speed
# GPIO.output(6,GPIO.LOW)  # Move Forward
distance = 0
j = 0 
msgLat = 0
msgLon = 0
apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(-6.90797266607928, 107.7761143223271, 14, apikey=apikey)
port=serial.Serial("/dev/ttyUSB0", 9600)

def mySteer(lat1, lon1, lat2, lon2,distances) :
    dlat = lat2-lat1
    dlon = lon2-lon1
    X =  cos(lat2) * sin(dlon)
    Y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    bearing = atan2(X,Y)
    bearing = ((degrees(bearing)+360)%360)    
    hmc5883l = i2c_hmc5883l.i2c_hmc5883l(0)
    (heading, minutes) = hmc5883l.getHeading()
    
    degree = bearing - heading

    if (degree > 0) : # belok kanan
        GPIO.output(20,GPIO.HIGH)
        GPIO.output(21,GPIO.LOW)

    elif (degree < 0) : #belom kiri
        GPIO.output(21,GPIO.HIGH)
        GPIO.output(20,GPIO.LOW)
    print (distances)
    for (i in range int(distances)):
        GPIO.output(6,GPIO.LOW)

    GPIO.cleanup()

def myDistance(lat1, lon1, lat2, lon2,distances) :
    coords_1 = (lat1,lon1)
    coords_2 = (lat2, lon2)
    distance = geopy.distance.distance(coords_1, coords_2).m  
    # distance = hs.haversine(loc1,loc2)*1000
    # distances = float(distance) + float(distances)
    return distances


try:
  mdata = port.readline().decode().strip()
  if "$GPGGA" in mdata:
    msg = nmea.parse(mdata)
    msgLat = msg.latitude 
    msgLon = msg.longitude

  coord = []
  hfile = open("data.txt","r")
  distances = 0

  while True:
    line = hfile.readline()
    if not line:
        break
    line = line.strip().split(",")
    coord.append(line)
    
  for (i,c) in enumerate (coord) :
    if (i == 0) :
        lat1 = msgLat
        lon1 = msgLon
        lat2 = float(coord[i][0])
        lon2 = float(coord[i][1])
    try :
      lat1 = float(coord[i][0])
      lon1 = float(coord[i][1])
      lat2 = float(coord[i+1][0])
      lon2 = float(coord[i+1][1])
    except IndexError :
      lat2,lon2 = lat1, lon1

    distances = myDistance(lat1, lon1, lat2, lon2, distances)

    if (distances > 1) :
      print (distances)
      if ( i-j == 0 ):
         lat1 = float(coord[i-j][0])
         lon1 = float(coord[i-j][1])
      else :
        lat1 = float(coord[i-j+1][0])
        lon1 = float(coord[i-j+1][1])

      mySteer(lat1,lon1,lat2,lon2,distances)
      # print (lat1,lon1,lat2,lon2,distances)
      distances = 0
      j = 0
       
    j = j+1

except (KeyboardInterrupt, SystemExit):
#  port.close()
  print("Selesai")