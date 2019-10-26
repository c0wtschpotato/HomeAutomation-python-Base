#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#requirements for broadlink python from https://github.com/mjg59/python-broadlink, git clone git://github.com/xkonni/raspberry-remote.git ##forked to own git repo , make send and go
#sudo apt-get install libzbar-dev libzbar0 libffi-dev libssl-dev raspberry-remote wiringpi
#pip configparser


import os
from termcolor import colored

print ("installing depencies")
os.system("sudo apt-get install install libzbar-dev libzbar0 libffi-dev libssl-dev wiringpi")

print ("installing configparser")
os.system("sudo pip install configparser")
print ("installing git and python broadlink")
os.system ("sudo apt-get install git")
os.system("sudo git clone https://github.com/mjg59/python-broadlink")
r  = os.system("sudo chmod +x /home/pi/python-broadlink/setup.py")
if r == 0:
	os.system("sudo /home/pi/python-broadlink/./setup.py install")
else:
	print colored("python-broadlink could not be installed via setup.py pls retry yourself")

print("cloning raspberry-remote")
os.system("sudo git clone git://github.com/xkonni/raspberry-remote.git")
print("making send")
os.system("sudo /home/pi/raspberry-remote/./make send")
