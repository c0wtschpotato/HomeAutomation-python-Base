#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gpiozero import MotionSensor
from signal import pause
import paho.mqtt.client as mqtt
import time 
import datetime, astral, os
from astral.sun import sun
#os.system("DISPLAY=:0.0 chromium-browser 'http://192.168.1.103:8123/lovelace/default_view'")##open display to HASS 
HOST = "192.168.1.107"
try:## error catch for other pis but zero
    pir = MotionSensor(18)
except:
    print("not pi zero")
channel = input("Channel to post in (HomA/sensor/kitchen/move)")
observer = astral.Observer(longitude = 13.43809806362507 , latitude = 48.572195884199324  , elevation = 312)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/ledstrip1/get_status")## for internal comm
    client.subscribe("HomA/ledstrip1/set_status")
    client.subscribe("hermes/hotword/default/detected")##gets hermes action from snips and starts led strip
    client.subscribe("hermes/hotword/toggleOn")
    client.subscribe("c0wtschpotato:PCcontrol")
    client.subscribe("HomA/Philips/set_status")
    client.subscribe("HomA/sensor/kitchen/move")


def motion_function(channel): 
    client.publish(channel,1)
    if hotornot() is True:
        client.publish("gv2mqtt/light/3ACA983DAE115A38/command",'{"state":"ON"}')
        client.publish("gv2mqtt/light/D67AB08184CE6070/command",'{"state":"ON"}')
        print("published lights on"+str(datetime.datetime.now()))
    else:
        print("Movement but not night"+str(datetime.datetime.now()))
    set_display(1)

def no_motion_function(channel):
    client.publish(channel,0)
    if hotornot() is True and channel == "HomA/sensor/kitchen/move":
        client.publish("gv2mqtt/light/3ACA983DAE115A38/command",'{"state":"OFF"}')
        client.publish("gv2mqtt/light/D67AB08184CE6070/command",'{"state":"OFF"}')
        print("published movement stopped"+str(datetime.datetime.now()))

    else:
        print("Movement ended, but not night"+str(datetime.datetime.now()))
    set_display(0)

def set_display(state):
    print("State recieved",state)
    if state == 1:
        print("HDMI On")
        os.system("vcgencmd display_power 1")
        os.system("wlr-randr --output HDMI-A-1 --on")###newer PI OS
        os.system("wlr-randr --output HDMI-A-2 --on")
    else:
        os.system("vcgencmd display_power 0")
        os.system("wlr-randr --output HDMI-A-1 --off")
        os.system("wlr-randr --output HDMI-A-2 --off")###newer PI OS
        print("HDMI Off")
    print("\n")

def hotornot():
    d = datetime.datetime.utcnow() < astral.sun.sunrise(observer,datetime.datetime.today()+datetime.timedelta(days=1)).replace(tzinfo=None)### offset um 1 tag damit nicht der heutige sunrise verwendet wird
    m = datetime.datetime.utcnow() > astral.sun.sunset(observer).replace(tzinfo=None)
#    if d is True:
#        print("es ist vor Sonnenaufgang")
#    if m is True:
#        print("es ist nach Sonnenuntergang")
    if d is True and m is True:
        print("Es ist Nacht")
        return True
    print("EoF")

def on_message(client, userdata, msg):
    if msg.topic == 'HomA/sensor/kitchen/move':
        set_display(int(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
try:
    print("pi zero detected")
    pir.when_motion = motion_function
    pir.when_no_motion = no_motion_function
except:
    print("not pi zero")
client.on_message = on_message
client.connect(HOST, 1883, 60)
client.loop_forever()
