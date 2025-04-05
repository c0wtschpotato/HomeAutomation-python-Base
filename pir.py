#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gpiozero import MotionSensor
from signal import pause
import paho.mqtt.client as mqtt
import time 
import datetime, astral
from astral.sun import sun
import os

HOST = "192.168.1.107"
pir = MotionSensor(18)
observer = astral.Observer(longitude = 48.572195884199324, latitude = 13.43809806362507, elevation = 312)


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
    client.publish("HomA/kitchen/move",1)
    if hotornot() is True:
        client.publish("gv2mqtt/light/3ACA983DAE115A38/command",'{"state":"ON"}')
        client.publish("gv2mqtt/light/D67AB08184CE6070/command",'{"state":"ON"}')
        print("published lights on"+str(datetime.datetime.utcnow()))
    else:
        print("Movement but not night"+str(datetime.datetime.utcnow()))
    set_display(1)

def no_motion_function():
    client.publish("HomA/kitchen/move",0)
    if hotornot() is True:
        client.publish("gv2mqtt/light/3ACA983DAE115A38/command",'{"state":"OFF"}')
        client.publish("gv2mqtt/light/D67AB08184CE6070/command",'{"state":"OFF"}')
        print("published movement stopped"+str(datetime.datetime.utcnow()))

    else:
        print("Movement ended, but not night"+str(datetime.datetime.utcnow()))
    set_display(0)

def set_display(state):
    os.system("vcgencmd display_power ",state)


def hotornot():
    d = datetime.datetime.utcnow() < astral.sun.night(observer)[1].replace(tzinfo=None)
    m = datetime.datetime.utcnow() > astral.sun.night(observer)[0].replace(tzinfo=None)
#    if d is True:
#        print("es ist vor Sonnenaufgang")
#    if m is True:
#        print("es ist nach Sonnenuntergang")
    if d is True and m is True:
        print("Es ist Nacht")
        return True
    print("EoF")

def on_message(client, userdata, msg):
    if msg.topic == 'HomA/kitchen/move':
        print("Set state to",msg)
        set_display(msg)



client = mqtt.Client()
client.on_connect = on_connect
pir.when_motion = motion_function
pir.when_no_motion = no_motion_function
client.on_message = on_message
client.connect(HOST, 1883, 60)
client.loop_forever()