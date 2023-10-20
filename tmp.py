import sys
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 4
button2 = 22
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, GPIO.PUD_UP)

while True:
  curr = GPIO.input(button)
  curr2 = GPIO.input(button2)
  if curr == GPIO.HIGH and curr2== GPIO.HIGH:
    print ("HIGH")
  elif (curr == GPIO.HIGH and curr2 == GPIO.LOW):
    print ("RIGHT")
  elif(curr == GPIO.LOW and curr2 == GPIO.HIGH):
    print("LEFT")
  else:
    print("LOW")
  sleep(0.5)