import pygame
#file setup
path = "/home/pi/Documents/462Piano/piano/"
sound_files = ["1.wav", "2.wav", "3.wav", "4.wav", "5.wav", "6.wav", "7.wav", "8.wav", "9.wav", "10.wav", 
"11.wav", "12.wav", "13.wav", "14.wav", "15.wav", "16.wav", "17.wav", "18.wav"]

Key_PINS =[14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 2, 17, 27, 22, 5, 6, 13]
ABC_sequence=[14, 14, 24, 24, 25, 25, 24, 23, 23, 18, 18, 15, 15, 14, 24, 24, 23, 23, 18, 18, 15, 14, 14, 24, 24, 25, 25, 24, 23, 23, 18, 18, 15, 15, 14]
MaryNLamb_sequence = [ 18, 15, 14, 15, 18, 18, 18, 15, 15, 15, 18, 24, 24, 18, 15, 14, 15, 18, 18, 18, 15, 15, 18, 15, 14]
JingleBells_sequence = [18, 18, 18, 18, 18, 18, 18, 24, 14, 15, 18, 24, 24, 24, 24, 24, 18, 18, 18, 18, 15, 15, 18, 15, 24, 18, 18, 18, 18, 18, 18, 18, 24, 14, 15, 18, 24, 24, 24, 24, 24, 18, 18, 18, 18, 15, 15, 18, 15, 24]


#pygame setup
pygame.mixer.init()
speaker_volume = 0.5 #50% vol
pygame.mixer.music.set_volume(speaker_volume)

for k in JingleBells_sequence:
    i = Key_PINS.index(k)
    f = sound_files[i]
    pygame.mixer.music.load(path+f)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
