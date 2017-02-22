import RPi.GPIO as GPIO
import time

#Pin Definition
led1 = 18 #Broadcom pin 18, P1 pin 12
sound = 2 #Broadcom pin 2, P1 pin 3

#Pin Config
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(sound, GPIO.IN)

#Initial state for LEDs:
GPIO.output(led1, GPIO.LOW)

threshold = 400
print("Test, Crtl+C to quit")
try:
	
	while 1:
		svalue = GPIO.input(sound)
		print("Sound= "svalue)
		if 	svalue>threshold:
			GPIO.output(led1, GPIO.HIGH)
			time.sleep(0.5) 
		else:
			GPIO.output(led1, GPIO.LOW)
			time.sleep(0.5)
			

except KeyboardInterrupt:
	GPIO.cleanup()
