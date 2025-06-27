#led_brightness.py

import RPi.GPIO as GPIO

LED = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

pwm_led = GPIO.PWM(LED, 500)
pwm_led.start(100)

try:
	while (True):
		duty_s = input("Enter Brightness (0 to 100):")
		duty = int(duty_s)
		pwm_led.ChangeDutyCycle(duty)

except KeyboardInterrupt:
	pwm_led.stop()
	GPIO.cleanup()


