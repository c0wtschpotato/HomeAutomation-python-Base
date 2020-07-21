
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import os
import configparser, time, json

class MHZ():##Class for all MHZ controlled parts
 	"""docstring for MHZ"""
 	def __init__(self, address, units,status,name):
 		self.address = address
 		self.units = units
 		self.status = status
 		self.name = name
 	def set(self,status):
 		if status == "on" or status == "an":
 			status = "1"
 		if status == "off" or status == "aus":
 			status = "0"
 		os.system("sudo /home/pi/raspberry-remote/./send "+self.address+" " +self.units + " "+str(status))
 		self.status = status
 	def on(self):
 		os.system("sudo /home/pi/raspberry-remote/./send "+self.address+" " +self.units + " 1")
 	def off(self):
 		os.system("sudo /home/pi/raspberry-remote/./send "+self.address+" " +self.units + " 0")


mhz1 = MHZ("11001","1","0","philips")
mhz2 = MHZ("11001","2","0", "screen")
mhz3 = MHZ("11001","3","0", "led2")
mhz4 = MHZ("11001","4","0", "unused")
mhz5 = MHZ("11001","5","0","unused")

class HTS():
	"""docstring for ClassName"""
	# rmSendPath = "sudo python /home/pi/python-broadlink/cli/./broadlink_cli --type 0x2737 --host 192.168.1.104 --mac 65c55834ea34 --send "
	# os.system(rmSendPath+"@/home/pi/python-broadlink/cli/philips-up.vol_change")
	def __init__(self):
		self.name = "Samsung Home Theater"
		self.channel = "0"
		self.sendPath = "sudo python /home/pi/python-broadlink/cli/./broadlink_cli --type 0x2737 --host 192.168.1.104 --mac 65c55834ea34 --send "

	def volup(self):
		os.system(self.sendPath+"@/home/pi/python-broadlink/cli/philips-up.vol_change")

	def voldown(self):
		os.system(self.sendPath+"@/home/pi/python-broadlink/cli/philips-down.vol_change")

	def targetchannel(self,targetchannel):#0 hdmi, 1 fm, 2 bt, 3 apps, 4bd in, 5 aux
		i = abs(int(self.channel) - int(targetchannel))
		print("switching " + str(i) +" times")
		for j in range(0,i):
			print("swtich "+str(j))
			os.system(self.sendPath+"@/home/pi/python-broadlink/cli/philips-switch.source")
			time.sleep(1)
		
		
hts = HTS()



