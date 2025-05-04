
import os
try:
	import paho.mqtt.client as mqtt
except:
	os.system("pip install paho-mqtt")
####################################################
###########Commands#################################
#shutdown - shutdown machine#




HOST = input("Host IP:")
PORT = 1883
global channel
customchannel = input("Name the mqtt channel to listen to (HomA/remote/CHANNELNAME)")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/remote/%s" %customchannel)## for internal comm


def on_message(client, userdata, msg):
    if msg.topic == "HomA/remote/%s" %customchannel:
        msg.payload == "shutdown"
        print("Shutdown recieved")
        os.system("sudo shutdown now")






client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.51", 1883, 60)

client.loop_forever()