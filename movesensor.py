
import time,os
import RPi.GPIO as GPIO
   
# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 18 (GPIO 24) auf Input setzen
GPIO.setup(16, GPIO.IN)
low_count = 0
# Pin 11 (GPIO 17) auf Output setzen
#GPIO.setup(11, GPIO.OUT)

# Dauersschleife
while 1:
  # LED immer ausmachen
  #GPIO.output(11, GPIO.LOW)

  # GPIO lesen
  if GPIO.input(16) == GPIO.HIGH:
    # LED an
    #GPIO.output(11, GPIO.HIGH)
    print("gpio high")
    # Warte 100 ms
    os.system("vcgencmd display_power 1")
    time.sleep(0.1)
    low_count = 0
    # LED aus
    #GPIO.output(11, GPIO.LOW)

    # Warte 100 ms
    time.sleep(0.1)
  if GPIO.input(16) == GPIO.LOW:
                low_count = low_count +1
                print("screen off "+str(low_count))
                #os.system("vcgencmd display_power 0")
                time.sleep(0.1)
                if low_count >= 300:

                        while GPIO.input(16) == GPIO.LOW:
                                os.system("vcgencmd display_power$
                                print("sleeping")
                                time.sleep(0.5)