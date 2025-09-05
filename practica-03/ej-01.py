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
#Inicializaciòn de pines, todos en estado BAJO (apagados)
for n in pines:
	GPIO.setup(n, GPIO.OUT, initial=GPIO.LOW)

# El siguiente código hace parpadear los leds
while True: # Bucle infinito
	sleep(0.5)                 # Espera 500ms
	for n in pines:
    GPIO.output(n, GPIO.HIGH) # Enciende todos los leds del arreglo
	for n in pines:                 # Espera 500ms
    GPIO.output(n, GPIO.LOW)  # Apaga todos los leds del arreglo

