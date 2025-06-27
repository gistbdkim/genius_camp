#led_dimming.py

import RPi.GPIO as GPIO
import time

LED = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

LED = GPIO.PWM(LED, 100)

LED.start(0)

delay = 0.1

try:
	while (True):
		for i in range(0, 101):
			LED.ChangeDutyCycle(i)
			time.sleep(delay)
		for i in range(100, -1, -1):
			LED.ChangeDutyCycle(i)
			time.sleep(delay)

except KeyboardInterrupt:
	LED.stop()
	GPIO.cleanup()


