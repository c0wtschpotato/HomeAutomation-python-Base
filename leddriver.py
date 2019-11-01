import paho.mqtt.client as mqtt
import ws2801effects as ws
import json
import threading
do_run = ""
current_status = ""
HOST = '192.168.1.103'
PORT = 1883
current_status =""## init empty
last_status =""##empty, saves current to last before changing current

def loopfunc():###function used with threading to loop certain effects
	global last_status
        while do_run == True:
                ws.running_on_chain(ws.pixels,(44,44,44),(255,0,0),5,0.05)               
                ws.pixels.show()
                if do_run == False:
					if last_status !="free":
						last_status = json.loads(last_status)
						
					else:
						ws.pixels.clear()
						ws.pixels.show()
#                       break
                print("do run true")
                # ws.time.sleep(3)### stopper to stop flooding of console for debugging
        print("do run false")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/ledstrip1/get_status")## for internal comm
    client.subscribe("HomA/ledstrip1/set_status")
    client.subscribe("hermes/hotword/default/detected")##gets hermes action from snips and starts led strip
    client.subscribe("hermes/hotword/toggleOn")

def on_message(client, userdata, msg):
	global current_status, last_status
	last_status = current_status
	print(msg.topic + " "+ msg.payload)
	if msg.topic == "HomA/ledstrip1/set_status":
		print("ledstrip 1 status set: "+msg.payload+ "\n\n")
		current_status = msg.payload
		client.publish("HomA/ledstrip1",current_status)
		set_leds_to_input(current_status)
		print("last know status was "+ last_status)
		
	if msg.topic == "HomA/ledstrip1/get_status" :
		if msg.payload != "get":
			print("status called with "+msg.payload)			
		elif msg.payload =="get":
			print("published status "+current_status)
			client.publish(msg.topic,current_status)
	if msg.topic =='hermes/hotword/default/detected':
		### since no payload is transmitted here we create the wanted json object in this function
		
		global do_run
		do_run = True
		fake_payload ={
			"function":"running_on_chain",
			"basecolor":{"r":"55","g":"55","b":"55"},
			"runningcolor":{"r":"255","g":"0","b":"0"},
			"number_of_running":"5",
			"sleep_time":"0.1"
			}
		print("LED-Driver detected hotword from hermes")
		payload = json.dumps(fake_payload)
		t = threading.Thread(target=loopfunc,args=()).start()
		# client.publish("HomA/ledstrip1/set_status",current_status)
		# set_leds_to_input(payload)
	if msg.topic == "hermes/hotword/toggleOn":
		print("toggle on detected, stopping wake word animation")
		global do_run		
		do_run = False
		# client.publish("HomA/ledstrip1/set_status",current_status)		
		print("setting strip back to last status:\n "+ last_status)
		t.join()
		
	

def set_leds_to_input(sentpayload):
	print ("in set leds to input")
	obj = json.loads(sentpayload)
	# print(obj["function"])	
	if obj["function"] == "lightning":
		print("starting function lightning")
		ws.lightning(ws.pixels)
	if obj["function"] == "running_on_chain":
		# print(obj["basecolor"])
		# print(obj["runningcolor"])
		# print(obj["number_of_running"])
		# print(obj["sleep_time"])	
		ws.running_on_chain(ws.pixels,(int(obj["basecolor"]["r"]),int(obj["basecolor"]["g"]),int(obj["basecolor"]["b"])),(int(obj["runningcolor"]["r"]),int(obj["runningcolor"]["g"]),int(obj["runningcolor"]["b"])),int(obj["number_of_running"]),float(obj["sleep_time"]))
	if obj["function"] == "setalltocolor":
		ws.setalltocolor(ws.pixels,(int(obj["basecolor"]["r"]),int(obj["basecolor"]["g"]),int(obj["basecolor"]["b"])))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, 1883, 60)

client.loop_forever()


####textline just to push 