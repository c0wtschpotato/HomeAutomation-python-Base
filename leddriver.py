import paho.mqtt.client as mqtt

HOST = '192.168.1.103'
PORT = 1883
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/ledstrip1")

def on_message(client, userdata, msg):
	print(msg)
	print(msg.payload)
	if msg.topic == "HomA/ledstri1":
		print("ledstrip 1 angesprochen")
		if msg.payload == "status":
			print("returning status i last got")
		else:
			current_status = msg.payload
			print("set status to: %s", msg.payload)
		


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, 1883, 60)

client.loop_forever()


