#!/usr/bin/env python3
# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/

# Importa la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO
# Importa la función sleep del módulo time
from time import sleep
import threading

# Desactivar advertencias (warnings)
GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
GPIO.setmode(GPIO.BOARD)

pines = [ 12, 16, 18, 22, 31,  33, 32]
#Inicializaciòn de pines, todos en estado BAJO (apagados)
for n in pines:
	GPIO.setup(n, GPIO.OUT, initial=GPIO.LOW)

speed = 0.5

def pingPong():
	index = 0
	inc = 1
	while True: # Bucle infinito
		GPIO.output(pines[index], GPIO.HIGH)  # Enciende el primer led
		index = index + inc
		sleep(speed)
		#print(index)  
		if index == len(pines) or index < 0:
			index = index - inc
			inc = inc * (-1)
		else:
			GPIO.output(pines[index - inc], GPIO.LOW)
def entradaVelocidad():
	global speed
	while True:
		speed = int(input("ingrese la velocidad en [ms]:"))/1000

t1 = threading.Thread(target=pingPong)
t2 = threading.Thread(target=entradaVelocidad)

t1.start()
t2.start()

t1.join()
t2.join()

GPIO.cleanup()

		
