

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time,os
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

from datetime import datetime
fh = file('/dev/input/mice','r')

##Simply reads GPIO for movement and activates Screen
# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)
HOST = "192.168.1.107"
# Pin 18 (GPIO 24) auf Input setzen
GPIO.setup(16, GPIO.IN)
low_count = 0
high_count = 0
display = 0
idle_count = 0
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
    client.subscribe("HomA/sensor/kitchen/move")


client = mqtt.Client()
client.on_connect = on_connect
client.connect(HOST, 1883, 60)
# Dauersschleife
while 1:

  if GPIO.input(16) == GPIO.HIGH:
    #print(str(time.strftime("%H:%M:%S", time.localtime()))+" at Highcount:"+ str(high_count))
    # Warte 100 ms
    #time.sleep(0.1)
    low_count = 0
    high_count = high_count +1
    print(high_count)
    if high_count == 20 and display == 0:#display on if hightcount and it is off
        print(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")+" at Highcount "+str(high_count)))
        os.system("vcgencmd display_power 1")
        display = 1
        while True:##### Loop for at least 20 Secs after Mouse is moved and just then check again for Low on Movesens
            print(fh.read(3))
            time.sleep(1)
            if fh.read(3) == "":
                idle_count = idle_count +1
                print("no Movement"+str(idle_count))
            if idle_count >= 30:
                print("No movement, going to Idle")
                break
            print("Idlecount:")
            print idle_count

    if high_count in range(50,500,10): 
        #### What to do once a Movement is recognized, on exact number so only triggered once for movement
        
        client.publish("HomA/kitchen/move",1)


        #os.system("sudo fswebcam -r 1280x720 --no-banner /home/pi/HomeAutomation-python-Base/pictures/"+str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))+".jpg")
    # Warte 100 ms
    time.sleep(0.1)
  if GPIO.input(16) == GPIO.LOW:
                low_count = low_count +1
                #print(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")+" at Lowcount "+str(low_count)))
                #os.system("vcgencmd display_power 0")
                if low_count == 30:## reset high count if low sets in
                    print(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")+" at Lowcount "+str(low_count)))
                    high_count = 0
                time.sleep(0.1)
                if low_count >= 300:
                        client.publish("HomA/kitchen/move",0)
                        
                        os.system("vcgencmd display_power 0")
                        display = 0
                        sleep_start = (str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
                        print("sleeping since "+sleep_start)
                        while GPIO.input(16) == GPIO.LOW:
                                
                                high_count = 0
                                
                                time.sleep(0.5)




