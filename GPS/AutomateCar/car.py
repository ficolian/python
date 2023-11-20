import serial
import pynmea2 as nmea
import time
import gmplot
import math
from math import *
import RPi.GPIO as GPIO
import threading
from i2clibraries import i2c_hmc5883l


apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(-6.90797266607928, 107.7761143223271, 14, apikey=apikey)

nextPos = [-6.923956245639437,107.77407454771182]


port = serial.Serial("/dev/ttyUSB0", 9600)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)  # Steer Right
GPIO.setup(20,GPIO.OUT)  # Steer Left
GPIO.setup(16,GPIO.OUT)  # Control
GPIO.setup(6,GPIO.OUT)   # Move Forward
#GPIO.setup(xx,GPIO.OUT)   # Buzzer

GPIO.output(6,GPIO.HIGH) # Maju
#GPIO.output(xx,GPIO.LOW)   # Buzzer OFF

while True:
        currentPos = readGPS()
        nextHeading = getNextHeading(currentPos[0], currentPos[1], nextPos[0], nextPos[1]) 
        heading = readCompass
        degree = nextHeading - heading
        if (degree > 0) : # belok kanan
            GPIO.output(20,GPIO.HIGH)
            GPIO.output(21,GPIO.LOW)
        elif (degree < 0) : #belom kiri
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(20,GPIO.LOW)
        distance = getDistance(currentPos[0], currentPos[1], nextPos[0], nextPos[1])
        if (distance < 3) :
            print("Yeay, sudah sampaiii...")
        GPIO.output(6,GPIO.LOW) # Stop
        #GPIO.output(XX,GPIO.HIGH) #Buzzer ON
        break
        hfile = open("position.txt","a")
        hfile.write("%s,%s\n" % ( currentPos[0], currentPos[1], heading ))
        time.sleep(5)
        hfile.close()
GPIO.cleanup()

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
                       coord.append(msg.latitude,msg.longitude)
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
    dlat = lat2-lat1
    dlon = lon2-lon1
    X =  cos(lat2) * sin(dlon)
    Y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    heading = atan2(X,Y) #satuan masih radian
    heading = ((degrees(heading)+360)%360) #satuan dalam derajat
    return heading

def readCompass ():
    hmc5883l = i2c_hmc5883l.i2c_hmc5883l(0)
    (heading, minutes) = hmc5883l.getHeading()
    return heading

def getDistance(lat1, lon1, lat2, lon2) :
    x = sin((lat1-long1)/2)*sin((lat1-long1)/2)
    y = cos(lat1)*cos(long1)*sin((lat2-long2)/2)*sin((lat2-long2)/2)
    distance = 2*asin(sqrt(x+y))
    #distance = distance * 6371000/1000  # multiply by Earth radius to get kilometers
    distance = distance * 6371000  # multiply by Earth radius to get kilometers
    return distance