#!/usr/bin/env python3

import argparse
import logging
import sys
import time
import RPi.GPIO as GPIO
from time import sleep
from rpi_rf import RFDevice
GPIO.setmode(GPIO.BCM)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)


def send(code, gpio=26, pulselength=350, protocol=1, length=24, repeat=5):
    rfdevice = RFDevice(gpio)
    rfdevice.enable_tx()
    rfdevice.tx_repeat = repeat

    logging.info(str(code) +
                " [protocol: " + str(protocol) +
                ", pulselength: " + str(pulselength) +
                ", length: " + str(length) +
                ", repeat: " + str(rfdevice.tx_repeat) + "]")

    rfdevice.tx_code(code, protocol, pulselength, length)
    GPIO.setmode(GPIO.BCM)
    
def button_callback(channel):
    key_index = remoteButtonArr.index(channel)
    numToSend = key_index + 1000
    print("Button {} Pressed".format(numToSend))
    send(numToSend)
    

remoteButtonArr =[21, 20, 16, 12, 25, 24]
for b in remoteButtonArr:
  GPIO.setup(b, GPIO.IN, GPIO.PUD_UP)

# Setup event detection for buttons
for pin in remoteButtonArr:
    GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback, bouncetime=3000)
while True:
  sleep(0.000001)