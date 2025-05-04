
import os,json
try:
	import paho.mqtt.client as mqtt
except:
	os.system("pip install paho-mqtt")


####################################################
###########Commands#################################
#shutdown - shutdown machine#
config_file = 'config.json'

PORT = 1883
global customchannel,host


def create_or_read_config():
	if os.path.exists(config_file):
		with open(config_file, 'r') as file:
			config = json.load(file)
			print("Konfiguration geladen:")
			host= config['host']
			print(f"Host: {host}")
			customchannel =config['customchannel']
			print(f"Custom Channel: {customchannel}")
	else:
		host = input("Are you in Host network? y/n:")
		if host == "y":
			host = "192.168.1.107"
		else:
			host = "192.168.0.51"
		customchannel = input("Bitte geben Sie den Custom Channel ein: ")

		config = {
		    'host': host,
		    'customchannel': customchannel
		}

		with open(config_file, 'w') as file:
		    json.dump(config, file, indent=4)

		print("Konfiguration gespeichert.")

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("HomA/remote/%s" %customchannel)## for internal comm


def on_message(client, userdata, msg):
	if msg.topic == "HomA/remote/%s" %customchannel:
		if msg.payload == "shutdown":
			print("Shutdown recieved")
			os.system("sudo shutdown now")
		else:
			print("unknown message")




create_or_read_config()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, 1883, 60)

client.loop_forever()