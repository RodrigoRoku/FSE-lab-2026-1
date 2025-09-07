#!/usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)
pwm = GPIO.PWM(32, 1000)

pwm.start(0)
#Se  usaran retardos de 1ms por lo que cada ms el ciclo de trabajo debe incrementarse 100/1000
step =  1
flag = True
duty = 0  #Inicia apagado el led
encender = True 	
while flag:
	try:
		#dutyCycle = int(input("Duty cycle: "))
		#sleep(0.001)
		pwm.ChangeDutyCycle(duty)
		sleep(0.01)
		if encender:
			if duty < 100:
				duty = duty + step
				#sleep(0.5)
				#print(duty)
			else:
				sleep(0.5)
				#print("hai")
				encender = False 
		else: 
			if duty > 0:
				duty = duty - step
				#sleep(0.5)
				#print(duty)
			else:
				sleep(0.5)
				flag  = False
	except:
		flag = False
		pwm.ChangeDutyCycle(0)
	#end try
#end while
pwm.stop()
GPIO.cleanup()

