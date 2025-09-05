#!/usr/bin/env python3
# ## ###############################################
#
# pwm.py
# Blinks a led on pin 32 using Raspberry Pi
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################

# Importa la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO
# Importa la función sleep del módulo time
from time import sleep

# Desactivar advertencias (warnings)
GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
# Llame GPIO.setmode(GPIO.BCM) para usar el canal SOC definido por Broadcom
GPIO.setmode(GPIO.BOARD)
# ~ pines = [32, 33, 12, 16, 18, 22, 31]
pines = [ 12, 16, 18, 22, 31,  33, 32]
pines.reverse()
for n in pines:
	GPIO.setup(n, GPIO.OUT, initial=GPIO.LOW)
# Configurar el pin 32 como salida y habilitar en bajo

# ~ # El siguiente código hace parpadear el led
# ~ while True: # Bucle infinito
	# ~ inde
	# ~ sleep(0.5)                 # Espera 500ms
	# ~ for n in pines:
		# ~ GPIO.output(n, GPIO.HIGH) # Enciende el led
	# ~ sleep(0.5)
	# ~ for n in pines:                 # Espera 500ms
		# ~ GPIO.output(n, GPIO.LOW)  # Apaga el led
index = 0
speed = int(input("ingrese la velocidad en [ms]:"))/1000
while True: # Bucle infinito
	GPIO.output(pines[index], GPIO.HIGH)  # Apaga el led
	print(pines[index])
	index = (index + 1) % len(pines)
	sleep(speed)  
	if index != 0:
		GPIO.output(pines[index - 1], GPIO.LOW)
	else:
		GPIO.output(pines[len(pines)-1], GPIO.LOW)
		speed = int(input("ingrese la velocidad en [ms]:"))/1000
