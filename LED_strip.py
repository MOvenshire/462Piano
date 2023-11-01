# to run the code
# sudo pip3 install RPi.GPIO
# sudo pip3 install adafruit-circuitpython-neopixel
# sudo python3 LED_Strip.py

import RPi.GPIO as GPIO
import board
import neopixel
import time
import threading

# GPIO pins for the 18 Keys
Key_PINS = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23]  
LED_COUNT = 90
# The number of rows and columns in the LED matrix
ROWS = 18
COLS = 5

# LED strip: LED pin(pins on the raspberryPi), LED count(4x18), Brightness(0 for off 1 for on), auto write
strip = neopixel.NeoPixel(board.D18 , LED_COUNT, 1, False)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in Key_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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


###########################################
# light up from button to top
# this should be changed to display waht key should be triggered
# if the wrong key was pressed, 2 vertical line should be displayed, the maroon(correct) color, and the key pressed(white, maybe?)
def song_mode(key_index):
    global timer
    clear()
    row = key_index % ROWS
    for column in reversed(range(COLS)):
        index = row * COLS + column
        strip[index] = (128, 0, 0)  # Maroon color  
    strip.show()

    # Cancel existing timer and start a new one
    if timer is not None:
        timer.cancel()
    timer = threading.Timer(3.0, clear)  # Turn off LEDs after 3 seconds
    timer.start()




# Button callback function
def button_callback(channel):
    key_index = Key_PINS.index(channel)
    print("Button {} Pressed".format(key_index))
    play_mode(key_index)
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
