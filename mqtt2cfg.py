
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
HOST = 'localhost'
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

def on_message(client, userdata, msg):
    if msg.topic == 'hermes/hotword/default/detected':
        print("Wakeword detected!")
        global do_run
        do_run = True
        client.publish("HomA/ledstrip1/set_status",wakewordasjson)
        #t = threading.Thread(target=loopfunc,args=()).start()
    elif msg.topic == "hermes/hotword/toggleOn":
        print("Finished listening")
        client.publish("HomA/ledstrip1/set_status",settonormal)
        global do_run
        do_run = False

                                config = configparser.ConfigParser()
                                config.read(os.path.join(os.getcwd(), cfgpath))
                                config['philips']['vol_up'] = '0'
                                config['philips']['vol_down'] = '0'     
                                config['couchled']['brightness_up'] = '0'
                                config['couchled']['brightness_down'] = '0'             
                                with open(cfgpath, 'w') as configfile:
                                        config.write(configfile)


client = mqtt.Client()
client.on_connect = on_connect
do_run = True
client.on_message = on_message
client.connect(HOST, PORT, 60)
client.loop_forever()