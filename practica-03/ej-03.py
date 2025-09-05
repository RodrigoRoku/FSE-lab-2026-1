#!/usr/bin/env python3
# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/

# Importa la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO
# Importa la función sleep del módulo time
from time import sleep

# Desactivar advertencias (warnings)
GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
GPIO.setmode(GPIO.BOARD)

pines = [ 12, 16, 18, 22, 31,  33, 32]
pines.reverse(); #Cambia el sentido en que se recorre el arreglo
#Inicializaciòn de pines, todos en estado BAJO (apagados)
for n in pines:
	GPIO.setup(n, GPIO.OUT, initial=GPIO.LOW)

# El siguiente código hace parpadear el led
index = 0 #Indice para recorrer el arreglo
speed = int(input("ingrese la velocidad en [ms]:"))/1000
while True: # Bucle infinito
	GPIO.output(pines[index], GPIO.HIGH)  # Enciende el primer led
	print(pines[index])                   #Para fines de debugging
	index = index + 1
  #Revisa si se llegò al final del arreglo y reinicializa el ìndice
  if index >= len(pines):
    index = 0
	sleep(speed)  
	if index != 0:
		GPIO.output(pines[index - 1], GPIO.LOW)
	else:
		GPIO.output(pines[len(pines)-1], GPIO.LOW)
		speed = int(input("ingrese la velocidad en [ms]:"))/1000
