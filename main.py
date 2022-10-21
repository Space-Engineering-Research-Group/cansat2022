import cds
import GPS
import servo
import xbee_send
import DCmotor
import sys
import os
import time

light = cds.read()
GPS_get = GPS.Read_data()
f = open('home/pi/data/')

while True:
    xbee_send.send_message(str(GPS_get) + "/" + int(light))
    if(light > 1000):
        servo.role()
        time.sleep(5)