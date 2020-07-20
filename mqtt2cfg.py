
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import os
import configparser, time, json

HOST = "localhost"
PORT = 1883
cfgpath = "/var/lib/snips/skills/Snips-HomA/cfg.ini"
config = configparser.ConfigParser()
config.read(cfgpath)
print(config.sections())




def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    client.subscribe("hermes/hotword/default/detected")
    client.subscribe("hermes/hotword/toggleOn")
    client.subscribe("HomA/ledstrip1/get_status")
    client.subscribe("HomA/ledstrip1/set_status")
    client.subscribe("HomA/pc/cmd")
    client.subscribe("HomA/HTS/cmd")
    client.subscribe("HomA/433/cmd")
    print("subscribed to all Channels")

def on_message(client, userdata, msg):
	print("Message Inc "+msg.topic)
	# obj = msg.jsonloads(msg.payload)
	if msg.topic == 'hermes/hotword/default/detected':
		print("Wakeword detected!")
	elif msg.topic == "hermes/hotword/toggleOn":
		print("Finished listening")
	elif msg.topic == "HomA/433/cmd":
		print("433 MHZ: "+str(msg.payload))


                                # config = configparser.ConfigParser()
                                # config.read(os.path.join(os.getcwd(), cfgpath))
                                # config['philips']['vol_up'] = '0'
                                # config['philips']['vol_down'] = '0'     
                                # config['couchled']['brightness_up'] = '0'
                                # config['couchled']['brightness_down'] = '0'             
                                # with open(cfgpath, 'w') as configfile:
                                #         config.write(configfile)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, 1883, 60)
client.loop_forever()