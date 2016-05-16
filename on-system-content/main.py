#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# main.py
#
# Main (only) script the user must execute.
#  - Initializes hardware
#  - Checks connection to Google Sheets
#  - Starts TKinter
#  - Initializes MyGui and MyController classes

import time
import gspread
import json
import socket
import constants
from config import Data_Spreadsheet, Credentials_File
import RPi.GPIO as GPIO
import os
from gui import *
from controller import *
from oauth2client.client import GoogleCredentials

#---------- Main Script ----------

# setup GPIO using Board numbering
GPIO.setmode(GPIO.BCM)

# initialize GPIO pins and blink the lights once
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(pirPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.output(greenPin, True)
GPIO.output(redPin, True)
time.sleep(0.5)
GPIO.output(greenPin, False)
GPIO.output(redPin, False)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Credentials_File

credentials = GoogleCredentials.get_application_default()
credentials = credentials.create_scoped(['https://spreadsheets.google.com/feeds'])

print "\n"*50
print "Starting Up"
try: 
	root = Tk()
	mycontroller = MyController()
	mygui = MyGui(root, mycontroller)
	mycontroller.enableMotionDetect()
	print "Connecting to Google"
	gc = gspread.authorize(credentials)
	print "Opening sheet"
	wks = gc.open(Data_Spreadsheet).sheet1
	print "Set up and ready to go"
	root.mainloop()
	
except socket.gaierror:
	print "Could not connect to Google"
	root.mainloop()
except:
	print "Some error occurred"
	print sys.exc_info()

finally:
	print "Finished"
	GPIO.cleanup()
