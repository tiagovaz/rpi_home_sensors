#!/usr/bin/python3

# Added to cron: */4 * * * * /home/pi/rpi_home_sensors/dht11_data.py

import rrdtool
import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()


import time
import sys

def do_update():
  # read data using pin 4
  instance = dht11.DHT11(pin = 4)
  result = instance.read()
  timestamp = time.time()
  temp = str(result.temperature)
  humid = str(result.humidity)
  if result.is_valid():
    # in case of error, retry after 5 seconds
    for retry in (5, 1):
      try:
        if temp == "0":
            print("error fetching sensor data... trying again")
            time.sleep(1)
            continue
        print("updating db...", timestamp, temp, humid)
        rrdtool.update("/home/pi/rpi_home_sensors/templog.rrd",
                       "%d:%s:%s" % (timestamp,
                                       temp,
                                       humid))
        return
      except:
        print("retry in %is because of: ", retry)
        time.sleep(retry * 1000)
  else:
      print("Error getting sensor data: %d" % result.error_code)

do_update()
