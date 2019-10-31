import paho.mqtt.client as mqtt

HOST = '192.168.1.103'
PORT = 1883
current_status =""## init empty
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/ledstrip1/get_status")
    client.subscribe("HomA/ledstrip1/set_status")

def on_message(client, userdata, msg):
	global current_status
	if msg.topic == "HomA/ledstrip1/set_status":
		print("ledstrip 1 status set: "+msg.payload)
		current_status = msg.payload

		
	if msg.topic == "HomA/ledstrip1/get_status" 

		if msg.payload != "get":
			print("status called with "+msg.payload)
			
		elif: msg.payload =="get":
			print("published status "+current_status)
			client.publish(msg.topic,current_status)

		


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, 1883, 60)

client.loop_forever()


