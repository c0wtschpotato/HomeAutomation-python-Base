
import paho.mqtt.client as mqtt
import ws2801effects as ws
import json
import threading
from random import randrange
############################################################
######if all goes wrong, restart snips skil server##########
######before starting all over again, fucks shit up#########
############################################################
do_run = ""
current_status = ""
HOST = '192.168.1.103'
PORT = 1883
current_status =""## init empty
last_status = None
##empty, saves current to last before changing current

def loopfunc(input_payload):###function used with threading to loop certain effects
	global do_run
	r = randrange(0,255)
	g = randrange(0,255)
	b  = randrange(0,255)
	while do_run == True:
		ws.running_on_chain(ws.pixels,(r,g,b),(255 -r ,255-g,255-b),5,0.01)
	        if do_run == False:
				if last_status !="free":
					print("setting back leds")
					print(last_status)
					set_leds_to_input(last_status)
					return
				elif last_status == None:
					return
	return

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/ledstrip1/get_status")## for internal comm
    client.subscribe("HomA/ledstrip1/set_status")
    client.subscribe("hermes/hotword/default/detected")##gets hermes action from snips and starts led strip
    client.subscribe("hermes/hotword/toggleOn")

def on_message(client, userdata, msg):
	global do_run
	if msg.topic == "HomA/ledstrip1/set_status":
		global current_status
		global last_status
		print("ledstrip 1 status set: "+msg.payload+ "\n\n")
		current_status = msg.payload
		# client.publish("HomA/ledstrip1",current_status)###?! wtf
		last_status = current_status
		set_leds_to_input(current_status)
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
		### since no payload is transmitted here we create the wanted json object in this function
		print("hotword first")
		
		do_run = True
		print("LED-Driver detected hotword from hermes")
		t = threading.Thread(target=loopfunc,args=("testing arg",)).start()
		print("right after loop")
		# client.publish("HomA/ledstrip1/set_status",current_status)
		# set_leds_to_input(payload)
	if msg.topic == "hermes/hotword/toggleOn":
		global current_status
		print("toggle on detected, stopping wake word animation")
		do_run = False
		# client.publish("HomA/ledstrip1/set_status",current_status)		
		t.join()
		
	

def set_leds_to_input(sentpayload):
	print ("in set leds to input")
	obj = json.loads(sentpayload)	
	if obj["function"] == "lightning":
		print("starting function lightning")
		ws.lightning(ws.pixels)

	if obj["function"] == "running_on_chain":
		ws.running_on_chain(ws.pixels,(int(obj["basecolor"]["r"]),int(obj["basecolor"]["g"]),int(obj["basecolor"]["b"])),(int(obj["runningcolor"]["r"]),int(obj["runningcolor"]["g"]),int(obj["runningcolor"]["b"])),int(obj["number_of_running"]),float(obj["sleep_time"]))

	if obj["function"] == "setalltocolor":
		ws.setalltocolor(ws.pixels,(int(obj["basecolor"]["r"]),int(obj["basecolor"]["g"]),int(obj["basecolor"]["b"])))
	if obj["function"] == "rainbow_colors":
		ws.rainbow_colors(ws.pixels,0.01)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, 1883, 60)

client.loop_forever()


####textline just to push 