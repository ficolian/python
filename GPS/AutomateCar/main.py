import serial
import pynmea2 as nmea
import time
import gmplot
import math
from math import *
import RPi.GPIO as GPIO
import threading
from i2clibraries import i2c_hmc5883l
import haversine as hs
import geopy


apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(-6.90797266607928, 107.7761143223271, 14, apikey=apikey)

nextPos = ["-6.923956245639437,107.77407454771182",
           "-6.92417561587758,107.77417789196718",
           "-6.925795416083805,107.77495700269544",
           "-6.927184965862308,107.77555803822081",
           "-6.928240758711511,107.77597520957843"]

nPoint = 5
indexPoint = 0

port = serial.Serial("/dev/ttyUSB0", 9600)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)  # Steer Right
GPIO.setup(19,GPIO.OUT)  # Steer Left
#GPIO.setup(6,GPIO.OUT)  # Control
GPIO.setup(16,GPIO.OUT)   # Move Forward
#GPIO.setup(xx,GPIO.OUT)   # Buzzer

GPIO.output(16,GPIO.LOW)
time.sleep(2)# Maju
#GPIO.output(xx,GPIO.LOW)   # Buzzer OFF

def readGPS() :
    try:
        while True:
            try:
                mdata = port.readline().decode().strip()
                try:
                    #print(mdata)
                    if "$GPGGA" in mdata:
                        msg = nmea.parse(mdata)
                        print(msg.latitude, msg.longitude)
                        coord = []
                        coord.append(msg.latitude)
                        coord.append(msg.longitude)
                        return coord
                except serial.SerialException as e:
                    print("Device error: {}". format(e))
                    break
            except nmea.ParseError as e:
                print("Parse error: {}".format(e))
                break
    except (KeyboardInterrupt, SystemExit):
        port.close()
        print("Selesai")
        
def getNextHeading(lat1, lon1, lat2, lon2) : #lat2 --> tujuan, #lat1 --> posisi saat ini
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    X =  cos(lat2) * sin(dlon)
    Y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    heading = atan2(X,Y)#satuan masih radian
    heading = math.degrees(heading)
    compass_bearing = (heading + 360) % 360 #satuan dalam derajat
    return compass_bearing

def readCompass ():
    hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
    hmc5883l.setContinuousMode()
    hmc5883l.setDeclination(0, 0)
    (heading, minutes) = hmc5883l.getHeading()
    return heading

def getDistancebyHaversine(lat1, lon1, lat2, lon2) :
    loc1 = (lat1, lon1)
    loc2 = (lat2, lon2)
    distance = hs.haversine(loc1,loc2)*1000
    return distance

while True:
        currentPos = readGPS()
        nextHeading = getNextHeading(currentPos[0], currentPos[1], nextPos(indexPoint[0]), nextPos(indexPoint[1])) 
        heading = readCompass()
        degree = nextHeading - heading
        print("degree",degree)
        if (degree > 0) : # belok kanan
            print("belok kanan")
            GPIO.output(21,GPIO.LOW)
            time.sleep(2)
            GPIO.output(21,GPIO.HIGH)
        elif (degree < 0) : #belok kiri
            print("belok kiri")
            GPIO.output(19,GPIO.LOW)
            time.sleep(2)
            GPIO.output(19,GPIO.HIGH)
        distance = getDistancebyHaversine(currentPos[0], currentPos[1], nextPos(indexPoint[0]), nextPos(indexPoint[1]))
        indexPoint = indexPoint + 1
        if (indexPoint >= nPoint):
            print("Yeay, sudah sampaiii...")
            GPIO.output(16,GPIO.HIGH)
            time.sleep(2)# Stop
            #GPIO.output(XX,GPIO.HIGH) #Buzzer ON
            break
        hfile = open("position.txt","a")
        hfile.write("%s,%s,%s,%s,%s\n" % (currentPos[0], currentPos[1], degree, heading, distance))
        time.sleep(5)
        hfile.close()
        
GPIO.cleanup()

