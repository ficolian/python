import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)  # Steer Right
GPIO.setup(20,GPIO.OUT)  # Steer Left
GPIO.setup(16,GPIO.OUT)  # Control
GPIO.setup(6,GPIO.OUT)   # Move Forward
GPIO.setup(26,GPIO.OUT)  # Move Backward
GPIO.setup(12,GPIO.OUT)  # Speed

GPIO.output(6,GPIO.LOW)  # Move Forward

# loop:
#   baca posisi wahana
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
      gmap.polygon(*unpad_nangor, color='cornflowerblue', edge_width=10)
      gmap.draw('map3.html')

#   apakah posisi sesuai dengan rute referensi?
#   bila posisi ada di kiri rute referensi, 

	steer arahkan ke kanan
#     GPIO.output(20,GPIO.HIGH)
#     GPIO.output(21,GPIO.LOW)

#   bila posisi ada di kanan rute referensi, 

	steer arahkan ke kiri
#     GPIO.output(21,GPIO.HIGH)
#     GPIO.output(20,GPIO.LOW)
#   bila sudah tiba di tujuan
#     exit

GPIO.cleanup()