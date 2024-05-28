import RPi.GPIO as GPIO 
import os
from time import sleep 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 

print("Button is :", GPIO.input(25)) 


while True:
	print("Button is :", GPIO.input(25)) 
	if GPIO.input(25) == 1: 
		print("Laisser appuyer pour le reset !!") 
		print("Button is :", GPIO.input(25)) 
		sleep(2)
		if GPIO.input(25) == 1 :
			os.system('sudo reboot')
		else :
			print ("Pas de reset")
