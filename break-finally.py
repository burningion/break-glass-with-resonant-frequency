from threading import Thread
import pygame
import pyaudio
import numpy as np

import time

from voiceController import q, get_current_note

pygame.init()

screenWidth, screenHeight = 512, 512
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

running = True

titleFont = pygame.font.Font("assets/Bungee-Regular.ttf", 24)
titleText = titleFont.render("Hit the Glass Gently", True, (0, 128, 0))
titleCurr = titleFont.render("", True, (0, 128, 0))

noteFont = pygame.font.Font("assets/Roboto-Medium.ttf", 55)

t = Thread(target=get_current_note)
t.daemon = True
t.start()


low_note = ""
high_note = ""
have_low = False
have_high = True

noteHoldLength = 10  # how many samples in a row user needs to hold a note
noteHeldCurrently = 0  # keep track of how long current note is held
noteHeld = ""  # string of the current note

centTolerance = 10  # how much deviance from proper note to tolerate


def break_the_internet(frequency, notelength=.1):
    p = pyaudio.PyAudio()

    volume = 0.9     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = notelength   # in seconds, may be float
    f = frequency        # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

    # play. May repeat with different volume values (if done interactively)
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    stream.write(volume*samples)
    

newFrequency = 0
breaking = False
currentFrequency = 0
breaking_zone = False
super_breaking_zone = False
noteLength = 5.0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and newFrequency != 0:
            breaking = True
            currentFrequency = newFrequency - 10
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            noteLength = 30.0 
            breaking_zone = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            super_breaking_zone = True
            noteLength = 5.0

    screen.fill((0, 0, 0))

    if breaking:
        titleCurr = titleFont.render("Current Frequency: %f" % currentFrequency, True, 
                                     (128, 128, 0))
    
    # our user should be singing if there's a note on the queue
    else:
        if not q.empty():
            b = q.get()
            pygame.draw.circle(screen, (0, 128, 0), 
                               (screenWidth // 2 + (int(b['Cents']) * 2),300),
                               5)

            noteText = noteFont.render(b['Note'], True, (0, 128, 0))
            if b['Note'] == noteHeldCurrently:
                noteHeld += 1
                if noteHeld == noteHoldLength:
                    titleCurr = titleFont.render("Frequency is: %f" % b['Pitch'].frequency, True, 
                                                 (128, 128, 0))
                    newFrequency = b['Pitch'].frequency
            else:
                noteHeldCurrently = b['Note']
                noteHeld = 1
                screen.blit(noteText, (50, 400))

    screen.blit(titleText, (10,  80))
    screen.blit(titleCurr, (10, 120))
    pygame.display.flip()
    clock.tick(30)

    if breaking:
        break_the_internet(currentFrequency, noteLength)
