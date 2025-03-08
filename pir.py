#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gpiozero import MotionSensor
from signal import pause
import paho.mqtt.client as mqtt
import time 
import datetime, astral
from astral.sun import sun

HOST = "192.168.1.107"
pir = MotionSensor(18)
observer = astral.Observer(longitude = 48.572195884199324, latitude = 13.43809806362507, elevation = 312)

def initvar():
    global delay
    delay = 0

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
    global delay
    client.publish("HomA/move1",1)
    delay = 0
    if hotornot() is True:
        client.publish("gv2mqtt/light/3ACA983DAE115A38/command",'{"state":"ON"}')
        client.publish("gv2mqtt/light/D67AB08184CE6070/command",'{"state":"ON"}')
        print("published lights on")
    else:
        print("Movement but not night")

def no_motion_function():
    global delay
    if delay <= 5:
        delay += 1
        time.sleep(3)
        print("delayed {delay}")
        return
    client.publish("HomA/move1",0)
    client.publish("gv2mqtt/light/3ACA983DAE115A38/command",'{"state":"OFF"}')
    client.publish("gv2mqtt/light/D67AB08184CE6070/command",'{"state":"OFF"}')
    print("published movement stopped")

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


client = mqtt.Client()
client.on_connect = on_connect
initvar()
pir.when_motion = motion_function
pir.when_no_motion = no_motion_function
client.connect(HOST, 1883, 60)
client.loop_forever()



