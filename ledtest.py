import RPi.GPIO as GPIO
import time

#Pin Definition
vcc = 18 #Broadcom pin 18, P1 pin 12
led = 23 #Broadcom pin 23, P1 pin 16
dc= 95 #duty cycle (0-100)
s
#Pin Config
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(vcc, GPIO.OUT)
pwm = GPIO.PWM(vcc,50)

#Initial state for LEDs:
GPIO.output(led, GPIO.LOW)
pwm.start(dc)

print("Test, Crtl+C to quit")
try:
	while 1:
		pwm.ChangeDutyCycle(100-dc)
		GPIO.output(led, GPIO.HIGH)
		time.sleep(0.075)
		GPIO.output(led, GPIO.LOW)
		time.sleep(0.075)
except KeyboardInterrupt:
	pwm.stop()
	GPIO.cleanup()
