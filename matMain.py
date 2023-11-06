import sys
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Buttons C[middle], D, E, F, G, A, B, C, D, E, F, C#, D#, F#, G#, A#, C#, D#
# Buttons   1   2   3   4   5   6   7  8  9   10  11  12  13  14  15  16 17 18
buttonArr =[14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 17, 27, 22, 5, 6, 13]
for b in buttonArr:
  GPIO.setup(b, GPIO.IN, GPIO.PUD_UP)

while True:
  for b in buttonArr:
    
    curr = GPIO.input(b)
    if(curr == GPIO.HIGH):
      print(b)
  sleep(0.5)
