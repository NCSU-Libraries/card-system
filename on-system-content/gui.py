#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# gui.py
#
# Home to the MyGui class, used for:
#  - Setting up the screen
#  - Interacting directly with the Controller
#  - Spinning the server
#  - Receiving the ID# from the card readers, which act like USB keyboards

from Tkinter import *
from constants import *
from config import API_Users_URL, API_Key
import os
import sys
import subprocess
import time

class MyGui:
	def __init__(self, parent, controller):
		print "Initializing GUI"

		self.parent = parent
		self.myController = controller
		self.patronId = None
		self.admin_checked = False
		
		# code for full screen
		self._geom='200x200+0+0'
		parent.geometry("{0}x{1}+0+0".format(
        parent.winfo_screenwidth(), parent.winfo_screenheight()))

		#---------- Images ----------
		self.swipeImage = PhotoImage(file=directory+"swipe.gif")
		self.authImage = PhotoImage(file=directory+"authorizing.gif")
		self.grantedImage = PhotoImage(file=directory+"granted.gif")
		self.deniedImage = PhotoImage(file=directory+"denied.gif")
		self.goodbyeImage = PhotoImage(file=directory+"goodbye.gif")
		self.adminSwipeImage = PhotoImage(file=directory+"admin_swipe.gif")
		self.adminImage = PhotoImage(file=directory+"admin.gif")
		
		self.imageLabel = Label(image=self.swipeImage) # Images go on labels
		self.imageLabel.image = self.swipeImage # keep a reference
		
		#---------- ID Text Box ----------
		self.idTextBox = Text(self.parent)
		self.idTextBox.configure(width = 10, height = 1, takefocus = 1, font="-*-Arial-*-R-*--*-1-*-*-*-*-ISO8859-1", background=parent["bg"], foreground=parent["bg"], borderwidth=0, highlightthickness=0, insertbackground=parent["bg"])
		self.idTextBox.bind("<Return>", self.checkId)
		
		#---------- Bypass Button ----------
		self.bypassButton = Button(self.parent)
		self.bypassButton.configure(text = "", padx=150, pady=40, borderwidth=0)
		self.bypassButton.configure(activebackground = self.bypassButton.cget("background"))
		self.bypassButton.bind("<Button-1>", self.bypassSensor)

		#---------- Admin Button ----------
		self.adminButton = Button(self.parent)
		self.adminButton.configure(text = "Admin")
		self.adminButton.bind("<Button-1>", self.adminCallback)
		
		#---------- Admin Exit Button ----------
		self.adminExitButton = Button(self.parent)
		self.adminExitButton.configure(text = "Exit")
		self.adminExitButton.bind("<Button-1>", self.exitAdminScreen)
		
		#---------- Restart Button ----------
		self.restartButton = Button(self.parent)
		self.restartButton.configure(text = "Restart Program")
		self.restartButton.bind("<Button-1>", self.restartProgram)
		
		#---------- Reboot Button ----------
		self.sysRestartButton = Button(self.parent)
		self.sysRestartButton.configure(text = "Reboot Pi")
		self.sysRestartButton.bind("<Button-1>", self.rebootPi)
		
		#---------- Show IP Button ----------
		self.IPButton = Button(self.parent)
		self.IPButton.configure(text = "Show IP")
		self.IPButton.bind("<Button-1>", self.showIP)
		
		#---------- Message Label ----------
		self.msgLabel = Label(self.parent)
		self.msgLabel.configure(text = "", width = 20)


		# print "GUI Ready"

		self.drawMainScreen()
		try:
			self.spinServer()
		except:
			print "Couldn't spin server"
		

	#---------- Spin Server ----------
	# Keep the server spun up with a periodic request.
	def spinServer(self):
		self.myController.APIRequest(API_Users_URL)
		print "spinning"
		self.parent.after(serverSpinPeriod, self.spinServer)
		
#-----------------------------------
#----- GUI Management Functions-----
#-----------------------------------
		
	#---------- Draw Main Screen ----------
	# Draw the main screen.
	# All widgets have been created; this function merely
	# displays them.
	def drawMainScreen(self):
		self.imageLabel.grid(row=0, column=0, columnspan=2)
		self.idTextBox.grid(row=1, column=0)
		self.adminButton.grid(row=2, column=1)
		self.msgLabel.grid(row=2, column=0)	
		self.bypassButton.grid(row=3, column=0)
		self.refreshImage()
		
		self.idTextBox.focus_force()
	
	#---------- Draw Admin Screen ----------
	# Draw the Admin screen.
	# This involves removing the "Admin" button from view,
	# changing the image, and displaying 
	def drawAdminScreen(self):
		self.adminButton.grid_forget()
		self.IPButton.grid(row=1, column=1)
		self.restartButton.grid(row=2, column=1)
		self.sysRestartButton.grid(row=3, column=1)
		self.adminExitButton.grid(row=4, column=0)
	
	#---------- Exit Admin Screen ----------
	# Remove the buttons of the Admin screen.
	def exitAdminScreen(self, event):
		self.restartButton.grid_forget()
		self.sysRestartButton.grid_forget()
		self.IPButton.grid_forget()
		self.adminExitButton.grid_forget()
		self.displayMessage("")
		self.drawMainScreen()
				
#------------------------------------
#----- Image and text functions -----
#------------------------------------
			
	#---------- GUI Change Image ----------
	# Change the image to whatever the argument is
	def changeImage(self, newImage):
		self.imageLabel.configure(image = newImage)
		self.imageLabel.image = newImage
			
	#---------- GUI Refresh Image ----------
	# Refresh the image back to the original
	# "Please swipe a card".
	def refreshImage(self):
		self.changeImage(self.swipeImage)
			
	#---------- Delete the text in the ID text box ----------
	def cleanIdBox(self, event):
		self.idTextBox.delete("@0,0", "end")
		
	#---------- Display a Message ----------
	def displayMessage(self, message):
		self.msgLabel.configure(text = message)
		
#------------------------------
#----- Callback Functions -----
#------------------------------

	#---------- GUI Check ID ----------
	# Main callback for ID text box. See if the ID is in the
	# database; if it is, grant access, else deny access. 
	#
	# If the ID is prefixed with a semicolon, it's a swipe out,
	# so just turn on the green light and turn off the motion
	# detection for a few seconds.
	def checkId(self, event):
		self.patronId = self.idTextBox.get("current linestart", "current lineend")
		print self.patronId
		self.cleanIdBox(event)

		self.changeImage(self.authImage)
		self.parent.update()
		
		if self.patronId is not None and self.patronId != "":
			# ';' in the ID means it's a swipe out
			if ';' in self.patronId:
				self.changeImage(self.goodbyeImage)
				self.parent.update()
				self.patronId = self.patronId.strip(";")
				self.patronId = self.patronId.partition("=")[0]
				self.myController.checkId(self.patronId, 0) # 0 for out; also logs
				self.parent.after(imageSleep, self.refreshImage)
				self.myController.grantAccess(playSong, False)
			else:
				if self.myController.checkId(self.patronId, 1) is False: # 1 for in; also logs
					self.changeImage(self.deniedImage)
					self.parent.update()
					self.parent.after(imageSleep, self.refreshImage)
					self.myController.denyAccess(playSong)
					self.displayMessage("")
				else: 
					self.changeImage(self.grantedImage)
					self.parent.update()
					self.parent.after(imageSleep, self.refreshImage)
					self.myController.grantAccess(playSong, True)
					self.displayMessage("")
				
		else:
			self.displayMessage("")
		
	#---------- Admin Callback ----------
	# Callback for "Admin" button.
	# Change the callback for the ID Text Box to the 
	# checkAdmin function.
	def adminCallback(self, event):
		self.changeImage(self.adminSwipeImage)
		self.parent.update()
		
		self.idTextBox.bind("<Return>", self.checkAdmin)
		self.idTextBox.focus_force()
		
		print "Waiting for Admin Swipe"
		
		self.parent.after(5000, self.adminCheckTimeout)
		
	def adminCheckTimeout(self):
		if self.admin_checked == False:
			self.drawMainScreen()
			self.idTextBox.bind("<Return>", self.checkId)
		else:
			self.drawAdminScreen()
		
	#---------- GUI Check Admin ----------
	# This function is temporary callback for the ID Text Box.
	# It asks the controller if a user has admin rights, and sets
	# the variable self.admin_checked accordingly
	def checkAdmin(self, event):
		print "Checking for admin rights"
		
		userID = self.idTextBox.get("current linestart", "current lineend")
		self.cleanIdBox(event)
		
		self.idTextBox.bind("<Return>", self.checkId)
		
		if self.myController.APICheckAdmin(userID):
			self.drawAdminScreen()
			admin_checked = True
		else:
			self.drawMainScreen()
			admin_checked = False	
	
	#---------- GUI Restart Program ----------
	# Callback for "Restart Program" button.
	# Start a new instance of the script and kill this one
	def restartProgram(self, event):
		os.system('sudo python ' + directory + 'main.py &')
		self.parent.quit()
		
	#---------- GUI Reboot Pi ----------
	# Callback for "Reboot Pi" button.
	# Reboot the pi completely.
	def rebootPi(self, event):
		os.system('sudo reboot &')
		
	#---------- GUI Show IP ----------
	# Callback for "Show IP" button.
	def showIP(self, event):
		address = subprocess.check_output('hostname -I', shell=True)
		self.displayMessage(address)

	#---------- GUI Bypass Sensor ----------
	# Callback for hidden bypass button.
	def bypassSensor(self, event):
		self.myController.grantAccess(False, False)
		self.idTextBox.focus_force()
