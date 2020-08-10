#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#requirements for broadlink python from https://github.com/mjg59/python-broadlink, git clone git://github.com/xkonni/raspberry-remote.git ##forked to own git repo , make send and go
#sudo apt-get install libzbar-dev libzbar0 libffi-dev libssl-dev raspberry-remote wiringpi libffi-dev
#pip configparser


import os
import configparser, time, json
config = configparser.ConfigParser()
cfgpath = "/home/pi/HomeAutomation-python-Base/LED.cfg"

print ("installing depencies")
os.system("sudo apt-get install libzbar-dev libzbar0 libffi-dev libssl-dev wiringpi python-pip")
os.system("sudo pip3 install RPi.GPIO")
os.system("sudo pip3 install hermes")
os.system("sudo pip3 install broadlink")
os.system("sudo pip3 install board")
os.system("sudo pip3 install adafruit-circuitpython-ws2801")
print ("installing configparser & adafruit ws2801 driver")
os.system("sudo pip3 install configparser")
os.system("sudo pip3 install Adafruit_WS2801")
print ("installing git and python broadlink")
os.system("sudo git clone https://github.com/mjg59/python-broadlink")
r  = os.system("sudo chmod +x /home/pi/python-broadlink/setup.py")
if r == 0:
	os.system("sudo /home/pi/python-broadlink/./setup.py install")
else:
	print("python-broadlink could not be installed via setup.py pls retry yourself")

print("cloning raspberry-remote")
os.system("sudo git clone git://github.com/xkonni/raspberry-remote.git")
print("making send")
os.system("sudo /home/pi/raspberry-remote/./make send")
PixelCount = input("How many LEDs are on the strip?")
config['LED']["PixelCount"] = PixelCount
stripcount = input("Give the Strip a Number")
config['LED']["Stripcount"] = stripcount
 with open(cfgpath, 'w') as configfile:
 	config.write(configfile)