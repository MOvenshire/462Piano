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


#file setup for sound
path = "/home/pi/Documents/462Piano/piano/"
sound_files = ["1.ogg", "2.ogg", "3.ogg", "4.ogg", "5.ogg", "6.ogg", "7.ogg", "8.ogg", "9.ogg", "10.ogg", 
"11.ogg", "12.ogg", "13.ogg", "14.ogg", "15.ogg", "16.ogg", "17.ogg", "18.ogg"]


#pygame setup for sound
pygame.mixer.init()
speaker_volume = 0.5 #50% vol
pygame.mixer.music.set_volume(speaker_volume)

#Store recorded sounds
recorded_sounds = []

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

# Record index of played notes
def record_mode(key_index):
    recorded_sounds.append(key_index)

# Note: May need to use a separate thread for Pygame sound because it may interfere with the GPIO event detection

# Button callback function
def button_callback(channel):
    key_index = Key_PINS.index(channel)
    print("Button {} Pressed".format(key_index))
    play_sound(sound_files[key_index])
    play_mode(key_index)
    # When in record mode
    # if len(recorded_sounds) < 20:
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
