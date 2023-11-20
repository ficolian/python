import serial
import pynmea2 as nmea
import time
import gmplot
import math
from math import *
import RPi.GPIO as GPIO
import threading
from i2clibraries import i2c_hmc5883l
import numpy as np
from pykalman import KalmanFilter
import haversine as hs

apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(-6.90797266607928, 107.7761143223271, 14, apikey=apikey)

nextPos = ["-6.940298,107.764939",
           "-6.940353,107.764921",
           "-6.940398,107.764908",
           "-6.940404,107.764939",
           "-6.940328,107.764975"]

nPoint = 5
indexPoint = 0

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
        
gpsMeasurements = []
nArray = 5

def getGPSFiltered(gpsMeasurements) : 
    for i in range(nArray):
        gpsMeasurements.append(readGPS())
    #print(gpsMeasurements[0])
    initial_state_mean = [gpsMeasurements[0][0],
                          0,
                          gpsMeasurements[0][1],
                          0]

    transition_matrix = [[1, 1, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 1],
                         [0, 0, 0, 1]]

    observation_matrix = [[1, 0, 0, 0],
                          [0, 0, 1, 0]]

    kf1 = KalmanFilter(transition_matrices = transition_matrix,
                      observation_matrices = observation_matrix,
                      initial_state_mean = initial_state_mean)

    kf1 = kf1.em(gpsMeasurements, n_iter=5)
    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(gpsMeasurements)
    return smoothed_state_means
    
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

def getDistancebyHaversine(lat1, lon1, lat2, lon2) :
    loc1 = (lat1, lon1)
    loc2 = (lat2, lon2)
    distance = hs.haversine(loc1,loc2)*1000
    return distance

while True:
        currentPos = readGPS()
        coord2 = nextPos[indexPoint].split(',')
        lat2 = float(coord2[0])
        lon2 = float(coord2[1])
        gpsMeasurements.append(currentPos)
        gpsMeasurements.pop(0)
        currentPosFiltered = getGPSFiltered(gpsMeasurements)
        print(gpsMeasurements)
        print(currentPosFiltered[:,0])
        nextHeading = getNextHeading(currentPosFiltered[4][0], currentPosFiltered[4][1], lat2, lon2) 
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
        distance = getDistancebyHaversine(currentPosFiltered[4][0], currentPosFiltered[4][1], lat2, lon2)
        if (distance < 3) :
            indexPoint = indexPoint + 1
            if (indexPoint >= nPoint):
                print("Yeay, sudah sampaiii...")
                GPIO.output(16,GPIO.HIGH)
                time.sleep(2)# Stop
                #GPIO.output(XX,GPIO.HIGH) #Buzzer ON
                break
        hfile = open("position.txt","a")
        hfile.write("%s,%s,%s,%s\n" % (currentPosFiltered[4][0], currentPosFiltered[4][1], heading, distance))
        time.sleep(5)
        hfile.close()
        
GPIO.cleanup()