from picamera import PiCamera
import time
from gpiozero import LED
import RPi.GPIO as GPIO 
import os
from time import sleep 

led = LED(21)
led.on()
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 

print("Button is :", GPIO.input(25)) 
camera = PiCamera()
time.sleep(0.5)
led.off()
camera.resolution = (1920, 1080)
camera.vflip = True
camera.contrast = 10
camera.framerate = 30

while True:
	led.off()
#	print("Button is :", GPIO.input(25)) 
	if GPIO.input(25) == 1:
		for i in range (5) :
			led.on()
			file_name = "/home/pi/Pictures/video_" + str(time.time()) + ".h264"
			print("Start recording...")
			camera.start_recording(file_name)
			camera.wait_recording(2)
			camera.stop_recording()
			print("Done.")
			led.off()  





