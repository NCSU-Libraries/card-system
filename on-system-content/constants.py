#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# constants.py
#
# Constants and global variables to be used across multiple files

# to pass to denyAccess/grantAccess
playSong = 1
muteSong = 0

# GPIO pins used
greenPin = 27
redPin = 22
pirPin = 17

# other constants
accessSleep = 4 # seconds to leave an LED on
imageSleep = 2500 # milliseconds between image refreshes
motionSleep = .25 # seconds to wait after motion is detected
serverSpinPeriod = 90000 # milliseconds between calls to spinServer() in GUI
directory = '/home/pi/card_system/' # location of all .py .gif and .wav files

# Global variables
Todays_Date = ''
