
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
		self.channel = 0
		self.channelname = "HDMI"
		self.channels = {"HDMI":0,"FM":1,"BT":2,"APPS":3,"BD":4,"AUX":5}
		self.channelnameS = ["HDMI", "FM", "BT","APPS","BD","AUX"]
		self.sendPath = "sudo python /home/pi/python-broadlink/cli/./broadlink_cli --type 0x2737 --host 192.168.1.104 --mac 65c55834ea34 --send "

	def volup(self):
		os.system(self.sendPath+"@/home/pi/python-broadlink/cli/philips-up.vol_change")

	def voldown(self):
		os.system(self.sendPath+"@/home/pi/python-broadlink/cli/philips-down.vol_change")

	def targetchannel(self,targetchannel):#0 hdmi, 1 fm, 2 bt, 3 apps, 4bd in, 5 aux
		if targetchannel == "HDMI":
			targetchannel = self.channels["HDMI"]
		if targetchannel == "FM":
			targetchannel = self.channels["FM"]
		if targetchannel == "BT":
			targetchannel = self.channels["BT"]
		if targetchannel == "APPS":
			targetchannel = self.channels["APPS"]
		if targetchannel == "BD":
			targetchannel = self.channels["BD"]
		if targetchannel == "AUX":
			targetchannel = self.channels["AUX"]

		i = abs(int(self.channel) - int(targetchannel))
		print("switching " + str(i) +" times")
		for j in range(0,i):
			self.channel = int(self.channel)+1
			print("switched "+ str(j+1)+ " times. Now on " + str(self.channel))
			os.system(self.sendPath+"@/home/pi/python-broadlink/cli/philips.switch")
			if self.channel >= 6:
				self.channel = 0
				j = i
				print(" reached Channel 6 so its 0")
			if self.channel == int(targetchannel):
				print("channelname was "+str(self.channelname))
				self.channelname == str(self.channelnameS[int(self.channel)])
				print("and now is "+ str(self.channelname))
				break
			time.sleep(1)

		print("Selfchannel is targetchannel "+ self.channelnameS[int(self.channel)])
		
hts = HTS()



