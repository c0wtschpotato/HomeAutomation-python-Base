#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#requirements for broadlink python from https://github.com/mjg59/python-broadlink, git clone git://github.com/xkonni/raspberry-remote.git ##forked to own git repo , make send and go
#sudo apt-get install libzbar-dev libzbar0 libffi-dev libssl-dev raspberry-remote wiringpi libffi-dev
#pip configparser


import os
import configparser, time, json
config = configparser.ConfigParser()
cfgpath = "/home/pi/HomeAutomation-python-Base/LED.cfg"

def get_yes_or_no_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            print("Bitte geben Sie 'y' für Ja oder 'n' für Nein ein.")

print ("installing depencies")
try:
	os.system("sudo apt-get install libzbar-dev libzbar0 libffi-dev libssl-dev wiringpi python-pip")
try:
	os.system("sudo pip3 install RPi.GPIO")
try:
	#os.system("sudo pip3 install gpiozero")## only for pi zero
try:	
	os.system("sudo pip3 install hermes")
try:	
	os.system("sudo pip3 install broadlink")
try:	
	os.system("sudo pip3 install board")
try:	
	os.system("sudo pip3 install paho-mqtt")
try:	
	os.system("sudo pip3 install adafruit-circuitpython-ws2801")

try:
	print ("installing configparser & adafruit ws2801 driver")
	os.system("sudo pip3 install configparser")
try:	
	os.system("sudo pip3 install Adafruit_WS2801")
try:	
	os.system("sudo pip3 install astral")
try:	
	os.system("sudo pip3 install screen")
	print ("installing git and python broadlink")
try:	
	os.system("sudo git clone https://github.com/mjg59/python-broadlink")
	r  = os.system("sudo chmod +x /home/pi/python-broadlink/setup.py")
	if r == 0:
		os.system("sudo /home/pi/python-broadlink/./setup.py install")
	else:
		print("python-broadlink could not be installed via setup.py pls retry yourself")

print("cloning raspberry-remote")
if get_yes_or_no_input("Install raspi remote?") == "y":
	os.system("sudo git clone git://github.com/xkonni/raspberry-remote.git")
	print("making send")
	os.system("sudo /home/pi/raspberry-remote/./make send")
if get_yes_or_no_input("Use LED strips?") =="y":
	PixelCount = input("How many LEDs are on the strip?")
	config['LED']["PixelCount"] = PixelCount
	stripcount = input("Give the Strip a Number")
	config['LED']["Stripcount"] = stripcount
with open(cfgpath, 'w') as configfile:
	config.write(configfile)