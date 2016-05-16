#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# datalogger.py
# 
# Append makerspace usage statistics to a Google Spreadsheet
# Takes 5 arguments: date, timestamp (HH:MM), accessed (0 or 1), uniqueToday (0 or 1), 
#   and in or out (1 or 0, respectively).

import gspread
import sys
import os
from oauth2client.client import GoogleCredentials
from config import Data_Spreadsheet, Credentials_File

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Credentials_File

credentials = GoogleCredentials.get_application_default()
credentials = credentials.create_scoped(['https://spreadsheets.google.com/feeds'])

class MyDatalogger:
		
	def __init__(self, today, timestamp, accessed, unique, inOut):
		self.today = today
		self.timestamp = timestamp
		self.accessed = accessed
		self.unique = unique
		self.inOut = inOut
		self.values = [self.today, self.timestamp, self.accessed, self.unique, self.inOut]
		
		try:
			self.openSpreadsheet()
			self.performAppend()
		except:
			print "Logger Error:"
			print sys.exc_info()
		
	
	#---------- Open Spreadsheet ----------
	# Login to the Google account and open the spreadsheet and
	# worksheet (account and sheet info are in constants.py)
	def openSpreadsheet(self):
		self.gc = gspread.authorize(credentials)
		self.wks = self.gc.open(Data_Spreadsheet).sheet1
		
	#---------- Perform Append ----------
	# Update the appropriate cells.
	def performAppend(self):

		self.wks.append_row(self.values)	
		
		print "Appended to datalog"
		
# Main Script
		
if len(sys.argv) != 6:
	print "\nRequires 5 arguments: date, timestamp (HH:MM), access (0 or 1), uniqueToday(0 or 1), In/Out (1 or 0)\n"
	quit()

datalogger = MyDatalogger(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
