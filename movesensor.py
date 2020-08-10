

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time,os, datetime
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

##Simply reads GPIO for movement and activates Screen
# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)
HOST = "192.168.1.107"
# Pin 18 (GPIO 24) auf Input setzen
GPIO.setup(16, GPIO.IN)
low_count = 0
high_count = 0
# Pin 11 (GPIO 17) auf Output setzen
#GPIO.setup(11, GPIO.OUT)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("HomA/ledstrip1/get_status")## for internal comm
    client.subscribe("HomA/ledstrip1/set_status")
    client.subscribe("hermes/hotword/default/detected")##gets hermes action from snips and starts led strip
    client.subscribe("hermes/hotword/toggleOn")
    client.subscribe("c0wtschpotato:PCcontrol")
    client.subscribe("HomA/Philips/set_status")


client = mqtt.Client()
client.on_connect = on_connect
client.connect(HOST, 1883, 60)
# Dauersschleife
while 1:

  if GPIO.input(16) == GPIO.HIGH:
    print(str(time.strftime("%H:%M:%S", time.localtime()))+" at Highcount:"+ str(high_count))
    # Warte 100 ms
    time.sleep(0.1)
    low_count = 0
    high_count = high_count +1
    if high_count in range(0,500,10): 
        #### What to do once a Movement is recognized, on exact number so only triggered once for movement
        os.system("vcgencmd display_power 1")
        client.publish("HomA/kitchen/move",1)
        os.system("sudo fswebcam -r 1280x720 --no-banner /home/pi/HomeAutomation-python-Base/pictures/"+str(time.strftime("%H:%M:%S", time.localtime()))+"image.jpg")
    # Warte 100 ms
    time.sleep(0.1)
  if GPIO.input(16) == GPIO.LOW:
                low_count = low_count +1
                print(str(datetime.date.strftime("%d-%m-%Y %H:%M:%S", time.localtime()))+" at Lowcount "+str(low_count))
                #os.system("vcgencmd display_power 0")
                time.sleep(0.1)
                if low_count >= 300:
                        client.publish("HomA/kitchen/move",0)
                        os.system("vcgencmd display_power 0")
                        while GPIO.input(16) == GPIO.LOW:
                                
                                high_count = 0
                                print("sleeping")
                                time.sleep(0.5)




