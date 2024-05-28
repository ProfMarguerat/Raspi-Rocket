import time
from gpiozero import LED
import RPi.GPIO as GPIO 
import os
from time import sleep 

led_v = LED(23)
led_r = LED(20)
led_j = LED(21)

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

led_r.on()
time.sleep(0.2)
led_r.off()
led_j.on()
time.sleep(0.2)
led_j.off()
led_v.on()
time.sleep(0.2)
led_v.off()
led_r.on()

while True :
        led_r.on()


