import pygame
#file setup
path = "/home/pi/Documents/462Piano/piano_note_wav/"
sound_files = ["piano-e_E_major.wav", "piano-d_D_major.wav","piano-c_C_major.wav","piano-b_B_major.wav","piano-a_A_major.wav"]

#pygame setup
pygame.mixer.init()
speaker_volume = 0.5 #50% vol
pygame.mixer.music.set_volume(speaker_volume)

for f in sound_files:
    pygame.mixer.music.load(path+f)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
