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

nextPos = {'lat':-6.924671,'lng':107.772657}

port = serial.Serial("/dev/ttyUSB0", 9600)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)  # Steer Right
GPIO.setup(19,GPIO.OUT)  # Steer Left
GPIO.setup(6,GPIO.OUT)  # Control
GPIO.setup(16,GPIO.OUT)   # Move Forward
#GPIO.setup(xx,GPIO.OUT)   # Buzzer

GPIO.output(16,GPIO.LOW)
time.sleep(2)# Maju
#GPIO.output(xx,GPIO.LOW)   # Buzzer OFF

lat2 = nextPos['lat']
lon2 = nextPos['lng']

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
    dlat = lat2-lat1
    dlon = lon2-lon1
    X =  cos(lat2) * sin(dlon)
    Y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    heading = atan2(X,Y) #satuan masih radian
    heading = ((degrees(heading)+360)%360) #satuan dalam derajat
    return heading

def readCompass ():
    hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
    hmc5883l.setContinuousMode()
    hmc5883l.setDeclination(0, 0)
    (heading, minutes) = hmc5883l.getHeading()
    return heading

def getDistance(lat1, lon1, lat2, lon2) :
    x = sin((lat1-lon1)/2)*sin((lat1-lon1)/2)
    y = cos(lat1)*cos(lon1)*sin((lat2-lon2)/2)*sin((lat2-lon2)/2)
    distance = 2*asin(sqrt(x+y))
    #distance = distance * 6371000/1000  # multiply by Earth radius to get kilometers
    distance = distance * 6371000  # multiply by Earth radius to get kilometers
    return distance

while True:
        currentPos = readGPS()
        nextHeading = getNextHeading(currentPos[0], currentPos[1], lat2, lon2) 
        heading = readCompass()
        degree = nextHeading - heading
        if (degree > 0) : # belok kanan
            GPIO.output(19,GPIO.LOW)
            time.sleep(2)
            GPIO.output(19,GPIO.HIGH)
            print("belok kanan")
        elif (degree < 0) : #belok kiri
            GPIO.output(21,GPIO.LOW)
            time.sleep(2)
            GPIO.output(21,GPIO.HIGH)
            print("belok kiri")
        distance = getDistance(currentPos[0], currentPos[1], lat2, lon2)
        if (distance < 3) :
            print("Yeay, sudah sampaiii...")
            GPIO.output(16,GPIO.HIGH) # Stop
            #GPIO.output(XX,GPIO.HIGH) #Buzzer ON
            break
        hfile = open("position.txt","a")
        hfile.write("%s,%s,%s\n" % (currentPos[0], currentPos[1], heading))
        time.sleep(5)
        hfile.close()
        
GPIO.cleanup()