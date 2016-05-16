#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# controller.py
#
# Home to the MyController class, used for:
#  - Interacting directly with hardware: LEDs, PIR sensor
#  - Interacting directly with the SpaceAuth API and the datalogger script
#  - Checking IDs
#  - Granting/denying access

import time
import sys
import os
import subprocess
from constants import *
from config import *
import RPi.GPIO as GPIO
from urllib2 import urlopen, Request
from json import loads

class MyController:
	def __init__(self):
		print "Initializing controller"
		
		self.idList = []
		
	#---------- API Request ----------
	# Make an authorized request to the API using
	# the key found in constants.py
	def APIRequest(self, _url):
		_request = Request(_url, None, {'X-Api-Key':API_Key})
		return urlopen(_request)
				
	#---------- API Check Endorsement ----------
	# Endorsements are listed in a JSON file generated
	# by the web API.
	#
	# Arguments:
	#	user_id			: user id number to check
	#	endorsement_unique_name : unique name of endorsement in database 
	#	station			: station name ('enter', 'exit', etc.) in database
	# 
 	# Returns: 
	#	1 if user has endorsement, 0 otherwise
	#
	def APICheckEndorsement(self, user_id, endorsement_unique_name, station):
		try:
			endorsementsToParse = self.APIRequest(API_Users_URL + 
								user_id + 
								'/endorsements?station=' + 
								station).read()
		except Exception as e:
			print e
			print "Could not access server"
			return 0

		print endorsementsToParse
		parsedEndorsements = loads(endorsementsToParse)
		
		for endorsement in parsedEndorsements:
			if endorsement[Unique_Name_Key] == endorsement_unique_name:
				return 1
		
		return 0
		
	#---------- API Check Admin ----------
	# Returns 1 if user has admin access to the system, else 0.
	def APICheckAdmin(self, user_id):
		try:
			userToParse = self.APIRequest(API_Users_URL + user_id).read()
			parsedUser = loads(userToParse)
			if "admin" in parsedUser['role']:
				return 1
			else: 
				return 0
		except:
			print "Could not access server"
			return 0
		
	#---------- Check Date ----------
	# If today isn't the recorded date, erase the unique ID list
	# and set the date.
	def checkDate(self):
		global Todays_Date
		today = subprocess.check_output('date +"%D"', shell=True)
		today = today.strip()
		if Todays_Date != today:
			self.idList = []
			Todays_Date = today	
	
	# Get the current time
	def checkTime(self):
		timestamp = subprocess.check_output('date +"%H:%M"', shell=True)
		timestamp = timestamp.strip()
		
		return timestamp
		
	#---------- Controller Check ID ----------
	# See if the ID has space access and return True/False.
	# Append the swipe record to the Google Sheet.
	# Station: 0 for exit, 1 for enter
	def checkId(self, patronId, station):
		uniqueId = 0
		accessed = 0

		# Assign statin string
		if station == 1:
			stationStr = "enter"
		elif station == 0:
			stationStr = "exit"
		else: 
			return False

		accessGranted = self.APICheckEndorsement(patronId, Space_Access_Unique_Name, stationStr)
		if(accessGranted): accessGrantedBool = True
		else: 
			accessGrantedBool = False
			print patronId
		
		self.checkDate()
		
		# See if ID is unique for today
		# and if access was granted
		if patronId not in self.idList: 
			uniqueId = 1
			self.idList.append(patronId)
		else: uniqueId = 0

		# Get the current time
		timestamp = self.checkTime()
		
		# Build the shell command to run the datalogger
		dataloggerString = 'python '+directory+'datalogger.py "'+Todays_Date+'" "'+timestamp+'" "'+str(accessGranted)+'" "'+str(uniqueId)+'" "'+str(station)+'"&'
		
		subprocess.Popen(dataloggerString, shell=True)
		
		return accessGrantedBool
		
	#---------- Log Swipe Out ----------
	#
	#
	def logSwipeOut(self):

		self.checkDate()
		timestamp = self.checkTime()
		
		dataloggerString = 'python '+directory+'datalogger.py "'+Todays_Date+'" "'+timestamp+'" "'+'"1"'+'" "'+'"0"'+'" "'+'"0"'+'"&' 
		
		subprocess.Popen(dataloggerString, shell=True)
	
	#---------- Deny Access ----------
	# Play sad tune and blink the red light.
	# Disable motion detect for ~2.5 seconds.
	def denyAccess(self, toPlay):
		self.disableMotionDetect()
		GPIO.output(redPin, True)
		if toPlay:
			os.system('aplay ' + directory + 'sad.wav &')
		time.sleep(accessSleep)
		self.enableMotionDetect()
		GPIO.output(redPin, False)
		print "Access Denied"
		
	#---------- Grant Access ----------
	# Play happy tune and blink the green light.
	# Disable motion detect for ~4 seconds.
	def grantAccess(self, toPlay, inOrOut):
		self.disableMotionDetect()
		GPIO.output(greenPin, True)
		if toPlay:
			if inOrOut:
				os.system('aplay ' + directory + 'happy.wav &')
			else:
				os.system('aplay ' + directory + 'goodbye.wav &')
		time.sleep(accessSleep)
		self.enableMotionDetect()
		GPIO.output(greenPin, False)
		print "Access Granted"
		
	# Turn a specific pin on
	def LEDOn(self, LEDPin):
		GPIO.output(LEDPin, True)
		
	# Turn a specific pin off
	def LEDOff(self, LEDPin):
		GPIO.output(LEDPin, False)

	#---------- Motion Detected ----------
	# When motion is detected, play a beeping sound
	# and flash the red LED
	def motionDetectCallback(self, pirPin):
		print "Motion Detected!"
		os.system('aplay ' + directory + 'sad.wav &')
		while GPIO.input(pirPin):
			GPIO.output(redPin, True)
			time.sleep(motionSleep)
			GPIO.output(redPin, False)
			time.sleep(motionSleep)
	
	# Turn on motion detection
	def enableMotionDetect(self):
		GPIO.add_event_detect(pirPin, GPIO.RISING)
		GPIO.add_event_callback(pirPin, self.motionDetectCallback)
		
	# Turn off motion detectoin
	def disableMotionDetect(self):
		GPIO.remove_event_detect(pirPin)
