#!/usr/bin/python3

import rrdtool
import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 4
instance = dht11.DHT11(pin = 4)
result = instance.read()

import time
import sys

def do_update():
  timestamp = time.time()
  temp = str(result.temperature)
  humid = str(result.humidity)
# in case of error, retry after 5 seconds
  if result.is_valid():
    for retry in (5, 1):
      try:
        if temp == "0":
            print("error fetching sensor data... trying again")
            time.sleep(1)
            continue
        print("updating db...", timestamp, temp, humid)
        rrdtool.update("templog.rrd",
                       "%d:%s:%s" % (timestamp,
                                       temp,
                                       humid))
        return
      except:
        logging.exception("retry in %is because of: ", retry)
        time.sleep(retry * 1000)
  else:
      print("Error getting sensor data: %d" % result.error_code)

do_update()
