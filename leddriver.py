
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import ws2801effects as ws
import json
import threading
from random import randrange
import time,configparser
cfgpath = "/home/pi/HomeAutomation-python-Base/led.ini"
inipath = "/home/pi/HomeAutomation-python-Base/cfg.ini"

config = configparser.ConfigParser()
############################################################
######if all goes wrong, restart snips skil server##########
######before starting all over again, fucks shit up#########
############################################################
do_run = ""
current_status = ""
HOST = '192.168.1.107'
PORT = 1883
current_status =""## init empty
last_status = None
##empty, saves current to last before changing current

t = "emptythread"
def loopfunc(input_payload,pickfunc,opt = 0.0035):###function used with threading to loop certain effects// could be overruled by rereading retained mqtt messages
	global do_run
	r = randrange(0,120)
	g = randrange(0,255)
	b  = randrange(0,255)
	while do_run == True:
		if pickfunc == 1:
			ws.running_on_chain(ws.pixels,(r,g,b),(255 -r ,255-g,255-b),5,0.01)
		if pickfunc == 0:
			ws.rainbow_cycle(ws.pixels,opt)
		if do_run == False:
			if last_status !="free":
				
				# time.sleep(1)### wait a second to reset status
				if not "rainbow_colors" in last_status:
					print("setting back leds")
					print(last_status)
					set_leds_to_input(last_status)
				return
			elif last_status == None:
				return
	return

def loop_animation():##could loop by retained message
	cfg = config.read(os.path.join(os.getcwd(), cfgpath))
	print(cfg["loop"]["func"])
	for i in range(0,20):
		ws.rainbow_cycle(ws.pixels,0.05)
		if do_run == False:
			return

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/ledstrip1/get_status")## for internal comm
    client.subscribe("HomA/ledstrip1/set_status")
    client.subscribe("hermes/hotword/default/detected")##gets hermes action from snips and starts led strip
    client.subscribe("hermes/hotword/toggleOn")
    client.subscribe("c0wtschpotato:PCcontrol")
    client.subscribe("HomA/Philips/set_status")
    client.subscribe("gv2mqtt/light/2A8CB08184C4D3FC/command")

def on_message(client, userdata, msg):
	global do_run
	global t
	if msg.topic == "HomA/ledstrip1/set_status":
		global current_status
		global last_status
		print("ledstrip 1 status set: "+msg.payload+ "\n\n")
		current_status = msg.payload
		# client.publish("HomA/ledstrip1",current_status)###?! wtf
		last_status = current_status
		print("setting LEDs to input"+"\n")
		set_leds_to_input(current_status)
		print("Done"+"\n")
		# print("last know status was "+ last_status)

	if msg.topic == "HomA/ledstrip1/get_status" :
		global current_status
		if msg.payload != "get":
			print("status called with "+msg.payload)			
		elif msg.payload =="get":
			print("published status "+current_status)
			client.publish(msg.topic,current_status)

	if msg.topic =='hermes/hotword/default/detected':
		global current_status
		ursprung = json.loads(msg.payload)
		pickfunc = randrange(0,2)
		print("source: "+ursprung["siteId"])
		print("func to call: "+str(pickfunc))
		if do_run != True:
			do_run = True
			t = threading.Thread(target=loopfunc,args=("testing arg",pickfunc,)).start()
			# client.publish("HomA/ledstrip1/set_status",current_status)
			# set_leds_to_input(payload)
	if msg.topic == "hermes/hotword/toggleOn":
		global current_status
		print("toggleon activated, terminating threads")
		do_run = False
		t.join()

	if msg.topic == "HomA/Philips/set_status":
		obj = json.loads(msg.payload)
		cfg = config.read(os.path.join(os.getcwd(), inipath))
		print("MQTT Philips "+msg.payload)
		cfg['philips']['vol_up'] = '1'


def set_leds_to_input(sentpayload):
	print ("in set leds to input with" + sentpayload)
	global do_run
	global t

	obj = json.loads(sentpayload)	

	if obj ["function"] == "rainbow_slow":
		print("starting rainbow_slow")
		ws.rainbow_slow(ws.pixels)
		print("cycle done")
	if obj["function"] == "lightning":
		print("starting function lightning")
		ws.lightning(ws.pixels)

	if obj["function"] == "running_on_chain":
		ws.running_on_chain(ws.pixels,(int(obj["basecolor"]["r"]),int(obj["basecolor"]["g"]),int(obj["basecolor"]["b"])),(int(obj["runningcolor"]["r"]),int(obj["runningcolor"]["g"]),int(obj["runningcolor"]["b"])),int(obj["number_of_running"]),float(obj["sleep_time"]))

	if obj["function"] == "setalltocolor":
		ws.setalltocolor(ws.pixels,(int(obj["basecolor"]["r"]),int(obj["basecolor"]["g"]),int(obj["basecolor"]["b"])))

	if obj["function"] == "percentOfAll":
		print("in func percentOfAll")
		print(obj["percent"])
		print(int(obj["coloron"][0]),int(obj["coloron"][1]),int(obj["coloron"][2]))
		# ws.percentOfAll(ws.pixels,int(obj["percent"]),(int(obj["coloron"][0]),int(obj["coloron"][1]),int(obj["coloron"][2])),(int(obj["colorOff"][0]),int(obj["colorOff"][0]),int(obj["colorOff"][2])))
		ws.percentOfAll(obj["percent"],(int(obj["coloron"][0]),int(obj["coloron"][1]),int(obj["coloron"][2])),(int(obj["colorOff"][0]),int(obj["colorOff"][1]),int(obj["colorOff"][2])))

	if obj["function"] == "rainbow_colors":
		print("starting ranbow cycle")
		ws.rainbow_cycle(ws.pixels)
		do_run = False
		try: 
			t.join()
		except:
			pass
		do_run = True
		AnimationThread = threading.Thread(target = loop_animation,args=()).start()
	if obj["state"] == "ON":###attached to govee2mqtt
		ws.setalltocolor(ws.pixels,(int(obj["color"]["r"]),int(obj["color"]["g"]),int(obj["color"]["b"])))



	client.unsubscribe("HomA/ledstrip1/set_status")
	time.sleep(0.1)###so it doesnt loop too fast
	client.subscribe("HomA/ledstrip1/set_status")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, 1883, 60)

client.loop_forever()


####textline just to push 