#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gpiozero import MotionSensor
from signal import pause
import paho.mqtt.client as mqtt

HOST = "192.168.1.107"
pir = MotionSensor(18)
client = mqtt.Client()
client.on_connect = on_connect
client.connect(HOST, 1883, 60)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/ledstrip1/get_status")## for internal comm
    client.subscribe("HomA/ledstrip1/set_status")
    client.subscribe("hermes/hotword/default/detected")##gets hermes action from snips and starts led strip
    client.subscribe("hermes/hotword/toggleOn")
    client.subscribe("c0wtschpotato:PCcontrol")
    client.subscribe("HomA/Philips/set_status")
    client.subscribe("HomA/kitchen/move")

def motion_function():
    client.publish("HomA/move1",1)

def no_motion_function():
    client.publish("HomA/move1",0)

pir.when_motion = motion_function
pir.when_no_motion = no_motion_function
client.on_message = on_message
client.connect(HOST, PORT, 60)
client.loop_forever()


pause()


