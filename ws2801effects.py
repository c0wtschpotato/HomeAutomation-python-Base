# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, random
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
from random import randrange
import configparser
cfgpath = "/home/pi/HomeAutomation-python-Base/LED.cfg"
initcfg = configparser.ConfigParser()
initcfg.read(cfgpath)
# Configure the count of pixels:
PIXEL_COUNT = int(initcfg["LED"]["PixelCount"])
 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
#defekte Pixel 0,1,43
defekt = [0,1,43]
 
# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)
 
# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, wait=0.1):
    for i in range(pixels.count()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_cycle(pixels, wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)

def rainbow_slow(pixels, wait=0.05):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def rainbow_colors(pixels, wait=0.05):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((256 // pixels.count() + j)) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def brightness(pixels, affected_pixels = (0,PIXEL_COUNT),step=1,dec_or_inc = "decrease",exclude_color=(None,None,None)):
    # for j in range(int(256 // step)):
    if dec_or_inc == "decrease":
        for i in range(affected_pixels[0],affected_pixels[1]):
            r, g, b = pixels.get_pixel_rgb(i)
            if not "r" in exclude_color:
                r = int( r - step)
            if not "g" in exclude_color:
                g = int( g - step)
            if not "b" in exclude_color:
                b = int( b - step)
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
    if dec_or_inc == "increase":
        for i in range(affected_pixels[0],affected_pixels[1]):
            r, g, b = pixels.get_pixel_rgb(i)
            if not "r" in exclude_color:
                r = int(r + step)
            if not "g" in exclude_color:
                g = int(g + step)
            if not "b" in exclude_color:
                b = int(b + step)
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
    # pixels.show()
        # if wait > 0:
        #     time.sleep(wait)

 
def blink_color(pixels, blink_times=5, wait=0.5, color=(255,0,0)):
    for i in range(blink_times):
        # blink two times, then wait
        pixels.clear()
        for j in range(2):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)
 
def appear_from_back(pixels, color=(255, 0, 0)):
    pos = 0
    for i in range(pixels.count()):
        for j in reversed(range(i, pixels.count())):
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            # set then the pixel at position j
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.001)

def running_on_chain(pixels,basecolor = (255,255,255),runningcolor= (255,0,0),number_of_running=(5),sleep_time=(0.1)):
    global do_run
    for i in range(pixels.count()):
        pixels.set_pixel(i,Adafruit_WS2801.RGB_to_color(basecolor[0],basecolor[1],basecolor[2]))
    pixels.show()
    for i in range(pixels.count()):
        if i+number_of_running >= pixels.count():
            break
        for k in range(pixels.count()):
            pixels.set_pixel(k,Adafruit_WS2801.RGB_to_color(basecolor[0],basecolor[1],basecolor[2]))       
        
        for j in range(i,i+number_of_running):
            pixels.set_pixel(j,Adafruit_WS2801.RGB_to_color(runningcolor[0],runningcolor[1],runningcolor[2]))
            
        pixels.show()         
        time.sleep(sleep_time)
    #pixels.clear()
    #pixels.show()

def lightning(pixels):
    while 1:
        setalltocolor(pixels,(0,0,180))
        
        time.sleep(random.randrange(0,5))
        # time.sleep(4)
        which = random.randrange(0,PIXEL_COUNT-8)

        for i in range(which,which +8):
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(21,131,148))
        pixels.show()
        time.sleep(1)
        setalltocolor(pixels,(0,0,180))
        time.sleep(0.3)
        for i in range(which,which +8):
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(21,131,148))
        pixels.show()
        time.sleep(0.1)
        setalltocolor(pixels,(0,0,180))
        time.sleep(random.randrange(1,3))
        
def WaveOnAll(step = 10):
    global pixels
    for i in range(0,255,step):
        setalltocolor(pixels,(i,i,255))
        time.sleep(0.01)
#	print "step"
    for i in range(255,0,-1*step):
	setalltocolor(pixels,(255,i,i))
	time.sleep(0.01)
    for i in range(0,255,step):
	setalltocolor(pixels,(255-i*step,i,0))
	time.sleep(0.01)
#    print "finish"



def RandomHard(timing = 0.47):
    global pixels
    rndR = random.randrange(200,255,1)
    rndG = random.randrange(230,255,1)
    rndB = random.randrange(230,255,1)
    rndColor = random.randrange(1,4,1)
    print rndColor
    if rndColor == 1:
	setalltocolor(pixels,(rndR,255-rndG,255-rndB))
    if rndColor == 2:
	setalltocolor(pixels,(255-rndG,rndR,255-rndB))
    if rndColor > 2:
	setalltocolor(pixels,(255-rndG,255-rndB,rndR))
    time.sleep(timing)
        # pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(21,131,148))## hellblauer blitz
def burning(pixels,basecolor=(100,20,0), number_of_running= 15):

    setalltocolor(pixels,(int(basecolor[0]),int(basecolor[1]),int(basecolor[2])))
    startpixel = randrange(0,PIXEL_COUNT-number_of_running)

    for i in range(0,100):###maximum all pixels - number of changed
        brightness(pixels,(startpixel,startpixel + number_of_running),1,"increase",(None,"g","b"))
        pixels.set_pixel(randrange(startpixel,startpixel+number_of_running), Adafruit_WS2801.RGB_to_color(255,255,26))#set a random pixel to yellow
        time.sleep(0.2)
  
    for j in range(0,100):
        brightness(pixels,(startpixel,startpixel + number_of_running),1,"decrease",(None,"g","b"))
        pixels.set_pixel(randrange(startpixel,startpixel+number_of_running), Adafruit_WS2801.RGB_to_color(255,255,26))#set a random pixel to yellow
        time.sleep(0.1)        
    print("decreased spot")

    for j in range(0,60):
        brightness(pixels,(0,PIXEL_COUNT),1,"decrease",(None,"g","b"))
        time.sleep(0.0)
    print("decreased all")

    for j in range(0,60):
        brightness(pixels,(0,PIXEL_COUNT),1,"increase",(None,"g","b"))
        
        time.sleep(0.2)
    print("increased all")


def setalltocolor(pixels,color=(255,255,255),affected_pixels=(0,PIXEL_COUNT)):

    for i in range(affected_pixels[0],affected_pixels[1]):
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(color[0],color[1],color[2]))#
    pixels.show()

def percentOfAll(perc = 50,coloron=(255,255,255),colorOff= (0,0,0)):
    if perc <= 0:
        perc = 1
    if perc >= 100:
        perc = 100
    calcedCount = int(round(PIXEL_COUNT*(perc/100.0)))
    print(calcedCount)
    setalltocolor(pixels,colorOff,(calcedCount+1,PIXEL_COUNT))
    setalltocolor(pixels, coloron,(0,calcedCount))

        

def ColorWave(pixels,basecolor=(255,0,128),runningcolor=(255,0,0),number_of_running=10,sleep_time=(0.1),turns=5,brightness_diff=10):
    setalltocolor(pixels,(basecolor[0]/2,basecolor[1]/2,basecolor[2]/2))
    if (basecolor[0]/2)<brightness_diff:
        r = "r"
    else:
        r = None
    if (basecolor[1]/2)<brightness_diff:
        g = "g" 
    else:
        g = None
    if (basecolor[2]/2)<brightness_diff:
        b = "b"
    else:
        b = None
    if number_of_running % 2 == 0:
        MIDLED = round(number_of_running/2)
    else:
        MIDLED=round((number_of_running-1)/2)
    for i in range(-round((number_of_running/2)),turns):
        for j in range(1,PIXEL_COUNT+number_of_running):#######keine fucking ahnung
            brightness(pixels, (j,j+number_of_running-1),brightness_diff,"increase",(r,g,b))##light up all affected LEDs
            for k in range(j,):
                brightness(pixels, (j+round_down(number_of_running/4)),brightness_diff,"increase",(r,g,b))


 
if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!
 
    rainbow_cycle_successive(pixels, wait=0.1)
    rainbow_cycle(pixels, wait=0.01)
 
    brightness_decrease(pixels)
    
    appear_from_back(pixels)
    
    for i in range(3):
        blink_color(pixels, blink_times = 1, color=(255, 0, 0))
        blink_color(pixels, blink_times = 1, color=(0, 255, 0))
        blink_color(pixels, blink_times = 1, color=(0, 0, 255))
 
    
    
    rainbow_colors(pixels)
    
    brightness_decrease(pixels)
    
 
