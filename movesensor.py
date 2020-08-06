
import time,os
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.on_connect = on_connect
client.connect(HOST, 1883, 60)
##Simply reads GPIO for movement and activates Screen
# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

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
# Dauersschleife
while 1:

  if GPIO.input(16) == GPIO.HIGH:
    # LED an
    #GPIO.output(11, GPIO.HIGH)
    print("gpio high")
    # Warte 100 ms
    os.system("vcgencmd display_power 1")
    time.sleep(0.1)
    low_count = 0
    high_count = high_count +1
    if high_count == 5:
        #### What to do once a Movement is recognized, on exact number so only triggered once for movement
        client.publish("HomA/kitchen/move",1)
        os.system("sudo fswebcam -r 1280x720 --no-banner "+str(time.strftime("%H:%M:%S", time.localtime()))+"image.jpg")
    # Warte 100 ms
    time.sleep(0.1)
  if GPIO.input(16) == GPIO.LOW:
                low_count = low_count +1
                print("screen off "+str(low_count))
                #os.system("vcgencmd display_power 0")
                time.sleep(0.1)
                if low_count >= 300:
                        while GPIO.input(16) == GPIO.LOW:
                                os.system("vcgencmd display_power$")
                                client.publish("HomA/kitchen/move",0)
                                high_count = 0
                                print("sleeping")
                                time.sleep(0.5)