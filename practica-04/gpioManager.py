
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
		print("construyendo el objeto")
		#VAriables para controlar los bucles dentro de las funciones
		self.continueMainLoop = True
		self.continueFunctionLoop = True
		#Variables a través de las cuales se recibe el nombre de la función a ejecutar
		self.functionName = None
		self.functionArgument = None
		self.functionDictionary = {
			'led'		: self.leds,
			'marquee'	: self.marquee,
			'numpad'	: self.bcd,
			'stop'		: self.stop
		}
		# mapeado de nombres de funciones con sus "punteros"
		self.ledsRight = [ 12, 16, 18, 22, 31,  33, 32]
		self.ledsLeft = [32, 33, 31, 22 ,18 ,16, 12]
		self.pinesBcd = [36, 38, 40 ,37]
		


	def mainLoop(self):
		self.configureGPIO()
		while self.continueMainLoop:
			function = self.functionDictionary.get(self.functionName, None)
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
		GPIO.output(self.ledsLeft[num-1], GPIO.HIGH)
		#Para que no se siga llamando a la función.
		self.functionName = None
		self.functionArgument = None
	


	"""	Despliega en número proporcionado en el display de siete segmentos.
		(To be developed by the student)
	"""
	def bcd(self, num):
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
		elif type == 'left' or  type == 'right':
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
		index = 0
		inc = 1
		while self.continueFunctionLoop: # Bucle infinito
			GPIO.output(self.ledsLeft[index], GPIO.HIGH)  
			index = index + inc
			sleep(self.speed)
			#print(index)  
			if index == len(self.ledsLeft) or index < 0:
				index = index - inc
				inc = inc * (-1)
			else:
				GPIO.output(self.ledsLeft[index - inc], GPIO.LOW)

	#Limpieza del programa antes de finalizar el programa
	def stop(self):
		self.continueMainLoop = False
		self.continueFunctionLoop = False

	#Configuración de modo, pines y otros
	def configureGPIO(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		for led in self.ledsLeft:
			GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)

		for pin in self.pinesBcd:
			GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# manager = gpioManager()
# manager.functionName = "marquee"
# manager.functionArgument= "pingpong"
# manager.mainLoop()


	
