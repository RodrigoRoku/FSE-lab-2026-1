
# ## ###############################################
#
# gpio_manager.py
# Controla el gpio de la Raspberry pi 4
#
# Autor: Tapia Navarro Rodrigo y Hernández Alejo Ximena Gizell
# ## ###############################################

import RPi.GPIO as GPIO
from time import sleep

class gpioManager:

	speed = 0.5 #Para funciones de retardo
	


	def __init__(self):
		#VAriables para controlar los bucles dentro de las funciones
		continueMainLoop = True
		continueFunctionLoop = True
		#Variables a través de las cuales se recibe el nombre de la función a ejecutar
		functionName = None
		functionArgument = None

		# mapeado de nombres de funciones con sus "punteros"
		functionDictionary = {
			'leds'		: leds,
			'marquee'	: marquee,
			'bcd'			: bcd
			'stop'		: stop
		}

		ledsLeft = [ 12, 16, 18, 22, 31,  33, 32]
		ledsRight = [32, 33, 31, 22 ,18 ,16, 12]
		pinesBcd = [36, 38, 40 ,37]

def mainLoop(self):
	while self.continueMainLoop:
		function = self.functionDictionary.get(self.funcName, None)
		if function:
			self.continueFunctionLoop = True
			print('\tCall{}({})'.format(function, self.functionArgument))
			function(self.functionArgument)
	
	GPIO.cleanup()
	
def turnOffLeds(self):
	for led in self.ledsLeft:
		GPIO.output(led, GPIO.LOW)

""" Enciende el leds especificados en num, apagando los demás
	(To be developed by the student)
"""
def leds(self, num):
	self.turnOffLeds()
	GPIO.output(ledsLeft[num], GPIO.HIGH)
	#Para que no se siga llamando a la función.
	self.functionName = None
	self.functionArgument = None
	


"""	Despliega en número proporcionado en el display de siete segmentos.
	(To be developed by the student)
"""
def bcd(num):
	GPIO.output(36, GPIO.HIGH if (num & 0x00000001) > 0 else GPIO.LOW )
	GPIO.output(38, GPIO.HIGH if (num & 0x00000002) > 0 else GPIO.LOW )
	GPIO.output(40, GPIO.HIGH if (num & 0x00000004) > 0 else GPIO.LOW )
	GPIO.output(37, GPIO.HIGH if (num & 0x00000008) > 0 else GPIO.LOW )
	#Para que no se siga llamando a la función.
	self.functionName = None
	self.functionArgument = None


def marquee(self, type='pingpong'):
	self.turnOffLeds()
	if type == 'pingpong':
		self._marquee_pingpong()
	elif type == 'left':
		self._marquee(self.functionArgument)

def _marquee(self, orientation):
	if orientation == 'left':
		leds = self.ledsLeft
	else:
		leds = self.ledsRight

	index = 0
	while self.continueFunctionLoop: # Bucle infinito
		GPIO.output(leds[index], GPIO.HIGH)  # Enciende el  led
		index = index + 1
		#Revisa si se llegò al final del arreglo y reinicializa el ìndice
		if index >= len(leds):
			index = 0
		sleep(self.speed)  
		if index != 0:
			GPIO.output(leds[index - 1], GPIO.LOW)
		else:
			GPIO.output(leds[len(leds)-1], GPIO.LOW)

""" Activa el modo marquesina ping-pong"""
def _marquee_pingpong(self):
	pass

#Limpieza del programa antes de finalizar el programa
def stop(self):
	self.continueMainLoop = False
	self.continueFunctionLoop = False

#Configuración de modo, pines y otros
def configureGPIO(self):
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)

	for led in leds:
		GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)

	for pin in pinesBcd:
		GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)



	
