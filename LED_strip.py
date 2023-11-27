# to run the code
#libraries to install RPi.GPIO, pygame, adafruit-circuitpython-neopixel, rpi-rf all can be installed with sudo pip3 install
#python3 LED_Strip.py

import RPi.GPIO as GPIO
import board
import neopixel
import time
import threading
import pygame
import threading
import signal
import sys
import logging
from rpi_rf import RFDevice

### For Free Mode ####
from adafruit_led_animation.color import AMBER
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import (
    PURPLE,
    WHITE,
    AMBER,
    JADE,
    TEAL,
    PINK,
    MAGENTA,
    ORANGE,
)


# GPIO pins for the 18 Keys
# Buttons C[middle], D, E, F, G, A, B, C, D, E, F, C#, D#, F#, G#, A#, C#, D#
# Buttons   1   2   3   4   5   6   7  8  9   10  11  12  13  14  15  16 17 18
Key_PINS =[14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 2, 17, 27, 22, 5, 6, 13]

LED_COUNT = 90
# The number of rows and columns in the LED matrix
ROWS = 18
COLS = 5

# LED strip: LED pin(pins on the raspberryPi), LED count(4x18), Brightness(0 for off 1 for on), auto write
strip = neopixel.NeoPixel(board.D2 , LED_COUNT, 1, False)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in Key_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#file setup for sound
basepath ="/home/pi/Documents/462Piano/"
instrument = "piano"
path = basepath +instrument
sound_files = ["1.wav", "2.wav", "3.wav", "4.wav", "5.wav", "6.wav", "7.wav", "8.wav", "9.wav", "10.wav", 
"11.wav", "12.wav", "13.wav", "14.wav", "15.wav", "16.wav", "17.wav", "18.wav"]

#pygame setup for sound
pygame.mixer.init()
speaker_volume = 0.5 #50% vol

#Store recorded sounds
recorded_sequence = []
recording = False

# Timer for turning off LEDs
timer = None

#setup RF 
rfdevice = None

#setup learn modes 
ledModeArr = ['play', 'learn Mary', 'learn ABC', 'learn Jingle Bells', 'free']
currModeIndex = 0
ABC_sequence=[14, 14, 24, 24, 25, 25, 24, 23, 23, 18, 18, 15, 15, 14, 24, 24, 23, 23, 18, 18, 15, 14, 14, 24, 24, 25, 25, 24, 23, 23, 18, 18, 15, 15, 14]
MaryNLamb_sequence = [ 18, 15, 14, 15, 18, 18, 18, 15, 15, 15, 18, 24, 24, 18, 15, 14, 15, 18, 18, 18, 15, 15, 18, 15, 14]
JingleBells_sequence = [18, 18, 18, 18, 18, 18, 18, 24, 14, 15, 18, 24, 24, 24, 24, 24, 18, 18, 18, 18, 15, 15, 18, 15, 24, 18, 18, 18, 18, 18, 18, 18, 24, 14, 15, 18, 24, 24, 24, 24, 24, 18, 18, 18, 18, 15, 15, 18, 15, 24]

#Initialize each of the instruments
instruments = ['piano','guitar', 'violin']

##### HELPER FUNCTIONS 
#rx rf
def rfRXCode(gpio = 26):
    rfdevice = RFDevice(gpio)
    rfdevice.enable_rx()
    timestamp = None
    logging.info("Listening for codes on GPIO " + str(gpio))
    while True:
        if rfdevice.rx_code_timestamp != timestamp:
            timestamp = rfdevice.rx_code_timestamp
            logging.info(str(rfdevice.rx_code) +
                        " [pulselength " + str(rfdevice.rx_pulselength) +
                        ", protocol " + str(rfdevice.rx_proto) + "]")
            rfdevice.cleanup()
            return rfdevice.rx_code
        time.sleep(0.01)

#this function emulates a switch statement 
def handleRfRx(rxRFReturnVal):
    while True:
        if(rxRFReturnVal == 1000):
            currModeIndex = (currModeIndex + 1)%len(ledModeArr)
            #Note: case 0 handled in button detect bc it is relevant to button, these all operate individually while the mat does its own thing
            if(currModeIndex == 1):#learn Mary had a little lamb
                t1.start()
                t1.join()
            elif(currModeIndex == 2):#learn ABC
                t2.start()
                t2.join()
            elif(currModeIndex == 3):#learn Jingle Bells
                t3.start()
                t3.join()
            elif(currModeIndex == 4):#free design
                count = 0
                t4.start()
                t4.join()
        elif(rxRFReturnVal == 1001):#1001 (change instrument) 
                i = instruments.index(instrument)
                instrument = instruments[(i+1)%3]
                path = basepath + instrument

        elif(rxRFReturnVal == 1002): #1002 (start record)
                recorded_sequence = []
                recording = True

        elif(rxRFReturnVal == 1003): #1003 (play most recent record)
                for i in recorded_sequence:
                    play_sound(sound_files[i])
        elif(rxRFReturnVal == 1004): #1004 (volume up)
                speaker_volume += 0.2
        elif(rxRFReturnVal == 1005): #1005 (volume down)
                speaker_volume -= 0.2

def pollRfRx():
        while True:
        #poll RX
            retRX = rfRXCode()
            handleRfRx(retRX)
            time.sleep(0.5)

# Play sound associated with key pressed
def play_sound(sound_file):
    pygame.mixer.music.set_volume(speaker_volume)
    pygame.mixer.music.load(path + sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

### LED FUNCTIONS ###
# Clear all LEDs
def clear():
    for i in range(LED_COUNT):
        strip[i] = (0, 0, 0)
    strip.show()

# Light up from top to button
def play_mode(key_index):
    global timer
    clear()
    row = key_index % ROWS
    for col in range(COLS):
        index = row * COLS + col
        strip[index] = (128, 0, 0)  # Maroon color  
    strip.show()
    
    # Cancel existing timer and start a new one
    if timer is not None:
        timer.cancel()
    timer = threading.Timer(3.0, clear)  # Turn off LEDs after 3 seconds
    timer.start()


## Learn Mode ###
def play_key(strip, key_index, ROWS, COLS):
    global timer
    clear()
    row = key_index % ROWS
    for column in reversed(range(COLS)):
        index = row * COLS + column
        strip[index] = (128, 0, 0)  # Maroon color  
    strip.show()

    # Duration of the note and light
    time.sleep(0.5)

    # Turn off the LEDs in the row
    for column in reversed(range(COLS)):
        index = row * COLS + column
        strip[index] = (0, 0, 0)

    strip.show()


def learn_mode(strip, song_sequence, ROWS, COLS):
    for key_index in song_sequence:
        play_key(strip, key_index, ROWS, COLS)
        time.sleep(0.5)  # Delay between notes

### Free Mode ###
count = 0
def free_mode(speed=0.1, animation_duration=5, exit_condition= (count>40)):
    try:
        count+=1
        # Define animations with customizable parameters
        solid = Solid(strip, color=PINK)
        blink = Blink(strip, speed=speed, color=JADE)
        colorcycle = ColorCycle(strip, speed=speed, colors=[MAGENTA, ORANGE, TEAL])
        chase = Chase(strip, speed=speed, color=WHITE, size=3, spacing=6)
        comet = Comet(strip, speed=speed, color=PURPLE, tail_length=10, bounce=True)
        pulse = Pulse(strip, speed=speed, color=AMBER, period=3)

        animations = AnimationSequence(
            solid, blink, colorcycle, chase, comet, pulse,
            advance_interval=animation_duration,
            auto_clear=True,
        )

        while True:
            animations.animate()
            if exit_condition and exit_condition():
                break
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle specific errors if necessary

# Record index of played notes
def record_mode(key_index):
    recorded_sequence.append(key_index)

# Button callback function
def button_callback(channel):
    key_index = Key_PINS.index(channel)
    print("Button {} Pressed".format(key_index+1))
    play_sound(sound_files[key_index])
    
    if(recording == True and len(recorded_sequence)<20):
        record_mode(key_index)   
    if(len(recorded_sequence) == 19):
        recording == False

    #handle lights 
    match currModeIndex:
        case 0: #play
            play_mode(key_index)

def buttonLoop():
    while True:
        for b in Key_PINS:
            if(b == GPIO.LOW):
                key_index = Key_PINS.index(b)
                print("Button {} Pressed".format(key_index+1))
                play_sound(sound_files[key_index])
                if(recording == True and len(recorded_sequence)<20):
                    record_mode(key_index)   
                if(len(recorded_sequence) == 19):
                    recording == False
                #handle lights 
                if(currModeIndex == 0):#play
                        play_mode(key_index)
                time.sleep(1500) #most sound files are over 1 second 

#create threads
t1 = threading.Thread(target = learn_mode(strip, MaryNLamb_sequence, ROWS, COLS), daemon = True)
t2 = threading.Thread(target = learn_mode(strip, ABC_sequence, ROWS, COLS), daemon = True)
t3 = threading.Thread(target = learn_mode(strip, JingleBells_sequence, ROWS, COLS), daemon = True)
t4 = threading.Thread(target = free_mode(), daemon = True)
threadRfRx = threading.Thread(target = pollRfRx(), daemon = True)
buttonThread = threading.Thread(target = buttonLoop(), daemon = True)

# Main program loop
try:
    clear()
    print("Press a button to display a vertical line. Press CTRL+C to exit.")
    #both of these are infinite loops so no need to join threads. 
    buttonThread.start()
    threadRfRx.start()
    while True:
        time.sleep(0.5)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    if timer is not None:
        timer.cancel()  # Cancel the timer if it's running
    clear()
    GPIO.cleanup()
    rfdevice.cleanup()
    sys.exit(0)
