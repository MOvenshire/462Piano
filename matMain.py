import sys
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttonArr =[14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 17, 27, 22, 5, 6, 13, 19]
for b in buttonArr:
  GPIO.setup(b, GPIO.IN, GPIO.PUD_UP)

while True:
  for b in buttonArr:
    
    curr = GPIO.input(b)
    if(curr == GPIO.HIGH):
      print(b)
  sleep(0.5)