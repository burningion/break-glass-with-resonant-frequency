# # Breaking Wine Glasses with Python
#
# This is a re-production of an experiment from a blog post by Kirk Kaiser
# called [Breaking a Wine Glass in Python By Detecting the Resonant Frequency]
# (https://www.makeartwithpython.com/blog/break-glass-with-resonant-frequency/)
# for Boston University's PY104: Physics in Health Sciences.
#
# The goal is to reproduce the experiment and better understand how waves and
# resonant frequencies work, and talk about some of the ways this understanding
# of resonance could affect people in the field of Anatomy / Health Sciences.
# I went and made some style changes to the original code but the
# bulk of the functionality remains the same.
#
#
# - Freddie Vargus
# - PY104
# - Friday, April 27th, 2018

# We're using a Python 3.5 environment for this, and
# so we'll start off by importing some libraries we'll need.

# In[1]:


from threading import Thread
import pygame
import pyaudio
import numpy as np

import time

from voiceController import q, get_current_note


# The bulk of the work here is done by pygame, and pyaudio. Pygame is a
# cross-platform set of Python modules designed for writing video games.
#
# The main thing we care about here are the sound libraries, and we'll use
# a small GUI to display the frequencies which we'll be able to hear
# through our laptop's microphone.

# In[ ]:


pygame.init()


# In[ ]:


screen_width = 512
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


# In[ ]:


running = True

title_font = pygame.font.Font("assets/Bungee-Regular.ttf", 24)
title_text = title_font.render("Hit the Glass Gently", True, (0, 128, 0))
title_curr = title_font.render("", True, (0, 128, 0))

note_font = pygame.font.Font("assets/Roboto-Medium.ttf", 55)


# We'll want to run our audio code in a separate thread so that we have
# data coming in from the microphone and allow that
# data to be passed into the rest of our program.

# In[ ]:


t = Thread(target=get_current_note)
t.daemon = True
t.start()


# In[ ]:


low_note = ""
high_note = ""
have_low = False
have_high = True


# In[3]:


note_hold_length = 10  # how many samples in a row user needs to hold a note
note_held_currently = 0  # keep track of how long current note is held
note_held = ""  # string of the current note

cent_tolerance = 10  # how much deviance from proper note to tolerate


# In[ ]:


def break_things(frequency, note_length=.1):
    """
    Writes data to our audio output in order to break the glass.

    Parameters
    ----------
    frequency : int
        The frequency at which we'd like to produce our sounds
    note_length : int
        The duration of the note we'd like to play, in seconds

    Returns
    -------
    None
    """
    p = pyaudio.PyAudio()

    # range [0.0, 1.0]
    volume = 0.9
    # sampling rate in Hertz
    fs = 44100

    # in seconds, may be float
    duration = note_length
    # sine frequency in Hertz
    f = frequency

    # generate samples
    # and convert notes to a float32 array
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=fs,
        output=True
    )

    # 2pi * sampling rate * duration * frequency we want
    volume_value = 2 * np.pi * np.arange(fs * duration) * f
    print("Volume value: ", volume_value)
    samples = np.sin(volume_value / fs).astype(np.float32)

    # play the sound
    # we can repeat with different volume values
    # if we do this interactively
    stream.write(volume * samples)


# In[2]:


new_frequency = 0
breaking = False
current_frequency = 0
breaking_zone = False
super_breaking_zone = False
note_length = 8.0

# frequency resolution inversely proportional to duration


# In[ ]:


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
        if event.type == pygame.KEYDOWN and \
           event.key == pygame.K_SPACE and new_frequency != 0:
            breaking = True
            current_frequency = new_frequency - 10
            print("Hello")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            note_length = 30.0
            breaking_zone = True
            print("Hello")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            super_breaking_zone = True
            note_length = 5.0
            print("Hello")

    screen.fill((0, 0, 0))

    if breaking:
        titleCurr = title_font.render(
            "Current Frequency: %f" % current_frequency,
            True,
            (128, 128, 0)
        )

    # our user should be singing if there's a note on the queue
    else:
        if not q.empty():
            b = q.get()

            pygame.draw.circle(
                screen,
                (0, 128, 0),
                (screen_width // 2 + (int(b['Cents']) * 2), 300),
                5
            )

            note_text = note_font.render(b['Note'], True, (0, 128, 0))

            if b['Note'] == note_held_currently:
                note_held += 1
                if note_held == note_hold_length:
                    title_curr = title_font.render(
                        "Frequency is: %f" % b['Pitch'].frequency,
                        True,
                        (128, 128, 0)
                    )
                    new_frequency = b['Pitch'].frequency
            else:
                note_held_currently = b['Note']
                note_held = 1
                screen.blit(note_text, (50, 400))

    screen.blit(title_text, (10,  80))
    screen.blit(title_curr, (10, 120))
    pygame.display.flip()
    clock.tick(30)

    if breaking:
        break_things(current_frequency, note_length)
