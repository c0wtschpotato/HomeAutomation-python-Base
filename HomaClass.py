
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import os
import configparser, time, json

class MHZ():
 	"""docstring for MHZ"""
 	def __init__(self, address, units,status):
 		self.address = address
 		self.units = units
 		self.status = status
 	def set(self,status):
 		os.system("sudo /home/pi/raspberry-remote/./send "+self.address+" " +self.units + " "+str(status))
 		self.status = status



mhz1 = MHZ("11001","1","0")
mhz2 = MHZ("11001","2","0")
mhz3 = MHZ("11001","3","0")
mhz4 = MHZ("11001","4","0")
mhz5 = MHZ("11001","5","0")


class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		