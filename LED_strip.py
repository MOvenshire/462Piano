# to run the code
# sudo pip3 install RPi.GPIO
# sudo pip3 install adafruit-circuitpython-neopixel
# sudo python3 LED_Strip.py

import RPi.GPIO as GPIO
import board
import neopixel
import time
import threading

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
Key_PINS =[14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 17, 27, 22, 5, 6, 13]

LED_COUNT = 90
# The number of rows and columns in the LED matrix
ROWS = 18
COLS = 5

# LED strip: LED pin(pins on the raspberryPi), LED count(4x18), Brightness(0 for off 1 for on), auto write
strip = neopixel.NeoPixel(board.D2 , LED_COUNT, 1, False)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in Key_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(pin, GPIO.LOW)

#file setup for sound
path = "/home/pi/Documents/462Piano/piano/"
sound_files = ["1.ogg", "2.ogg", "3.ogg", "4.ogg", "5.ogg", "6.ogg", "7.ogg", "8.ogg", "9.ogg", "10.ogg", 
"11.ogg", "12.ogg", "13.ogg", "14.ogg", "15.ogg", "16.ogg", "17.ogg", "18.ogg"]

#pygame setup for sound
pygame.mixer.init()
speaker_volume = 0.5 #50% vol
pygame.mixer.music.set_volume(speaker_volume)

#Store recorded sounds
recorded_sequence = []

# Timer for turning off LEDs
timer = None


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


# Play sound associated with key pressed
def play_sound(sound_file):
    pygame.mixer.music.load(path+sound_file)
    pygame.mixer.music.play()


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


def learn_ABC_mode(strip, ABC_sequence, ROWS, COLS):
    ABC_sequence=[14, 14, 24, 24, 25, 25, 24, 23, 23, 18, 18, 15, 15, 14, 24, 24, 23, 23, 18, 18, 15, 14, 14, 24, 24, 25, 25, 24, 23, 23, 18, 18, 15, 15, 14]
    for key_index in ABC_sequence:
        play_key(strip, key_index, ROWS, COLS)
        time.sleep(0.5)  # Delay between notes

def learn_MaryNLamb_mode(strip, MaryNLamb_sequence, ROWS, COLS):
    MaryNLamb_sequence = [ 18, 15, 14, 15, 18, 18, 18, 15, 15, 15, 18, 24, 24, 18, 15, 14, 15, 18, 18, 18, 15, 15, 18, 15, 14]
    for key_index in MaryNLamb_sequence:
        play_key(strip, key_index, ROWS, COLS)
        time.sleep(0.5)  # Delay between notes

def learn_ABC_mode(strip, JingleBells_sequence, ROWS, COLS):
    JingleBells_sequence = [18, 18, 18, 18, 18, 18, 18, 24, 14, 15, 18, 24, 24, 24, 24, 24, 18, 18, 18, 18, 15, 15, 18, 15, 24, 18, 18, 18, 18, 18, 18, 18, 24, 14, 15, 18, 24, 24, 24, 24, 24, 18, 18, 18, 18, 15, 15, 18, 15, 24]
    for key_index in JingleBells_sequence:
        play_key(strip, key_index, ROWS, COLS)
        time.sleep(0.5)  # Delay between notes


### Free Mode ###
# update  the pin depending where the LED is connected
pixels = neopixel.NeoPixel(board.D6, LED_COUNT, 1, False)

def free_mode(speed=0.1, animation_duration=5, exit_condition=None):

    try:
        # Define animations with customizable parameters
        solid = Solid(pixels, color=PINK)
        blink = Blink(pixels, speed=speed, color=JADE)
        colorcycle = ColorCycle(pixels, speed=speed, colors=[MAGENTA, ORANGE, TEAL])
        chase = Chase(pixels, speed=speed, color=WHITE, size=3, spacing=6)
        comet = Comet(pixels, speed=speed, color=PURPLE, tail_length=10, bounce=True)
        pulse = Pulse(pixels, speed=speed, color=AMBER, period=3)

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
    print("Button {} Pressed".format(key_index))
    play_sound(sound_files[key_index])
    play_mode(key_index)
    # When in record mode
    # if len(recorded_sequence) < 20:
    #   record_mode(key_index)

    # when in song mode things change
    #song_mode(key_index)

# Setup event detection for buttons
for pin in Key_PINS:
    GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback, bouncetime=300)

# Main program loop
try:
    clear()
    print("Press a button to display a vertical line. Press CTRL+C to exit.")
    while True:
        time.sleep(0.1)  # Small delay to reduce CPU usage

finally:
    if timer is not None:
        timer.cancel()  # Cancel the timer if it's running
    clear()
    GPIO.cleanup()
