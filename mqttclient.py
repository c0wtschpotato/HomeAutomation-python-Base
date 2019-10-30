

PIXEL_COUNT = 50
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)



import paho.mqtt.client as mqtt
HOST = 'localhost'
PORT = 1883

def loopfunc():
        while do_run == True:
                ws2801effects.running_on_chain(pixels,(44,44,44),(255,0,0),5,0.05)
                pixels.clear()
                pixels.show()
                if do_run == False:
                        pixels.clear()
                        pixels.show()
#                       break
                print("do run true")
        print("do run false")
def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    client.subscribe("hermes/hotword/default/detected")
    client.subscribe("hermes/hotword/toggleOn")

def on_message(client, userdata, msg):
    if msg.topic == 'hermes/hotword/default/detected':
        print("Wakeword detected!")
        global do_run
        do_run = True
        t = threading.Thread(target=loopfunc,args=()).start()
    elif msg.topic == "hermes/hotword/toggleOn":
        print("Finished listening")
        global do_run
        do_run = False
        t.join()
client = mqtt.Client()
client.on_connect = on_connect
do_run = True
client.on_message = on_message
client.connect(HOST, PORT, 60)
client.loop_forever()
