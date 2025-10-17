# !/usr/bin/env python3
# ## ###############################################
#
# webserver.py
# Starts a custom webserver and handles all requests
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################
import os
import sys
import json
import magic
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import datetime
import smbus2
import struct
import time

# RP2040 I2C device address
SLAVE_ADDR = 0x0A # I2C Address of RP2040

# Name of the file in which the log is kept
LOG_FILE = './temp.log'

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

def readTemperature():
	try:
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)  # Performs write (read request)
		data = list(msg)   # Converts stream to list
		# list to array of bytes (required to decode)
		ba = bytearray()
		for c in data:
			ba.append(int(c))
		temp = struct.unpack('<f', ba)
		# print('Received temp: {} = {}'.format(data, temp))
		print('Temperatura: {} ºC'.format(round(temp[0], 2)))
		return round(temp[0], 2)
	except:
		return None


# Escribe la temperatura al archivo de log
def log_temp(temperature):
    if temperature is not None:
        try:
            with open(LOG_FILE, 'a') as fp:
                fp.write('{} {} °C\n'.format(
                    time.time(),
                    temperature
                ))
        except Exception as e:
            print("Error al guardar en log:", e)

def readTempFromSlave():
	#Limpiar el log, y abrir el archivo para almacenar los dato

	while True:
		try:
			cTemp = readTemperature()
			log_temp(cTemp)
			time.sleep(1)
		except KeyboardInterrupt:
			return

def readNLectures(numLecturas=20):
  with open(LOG_FILE, 'r') as fp:
    content = fp.read()
    content = content.strip()
    lecturas = content.split('\n')
    time = []
    temperature = []
    for n in lecturas:
      temp = n.split()
      fechaObj = datetime.datetime.fromtimestamp(float(temp[0]))
      fechaStr = f"{fechaObj.hour}:{fechaObj.minute}:{fechaObj.second}"
      time.append(fechaStr)
      temperature.append(float(temp[1]))
    time = time[-numLecturas:]
    temperature = temperature[-numLecturas:]

  return {
    "tiempos": time,
    "temperaturas": temperature
  }

# Nombre o dirección IP del sistema anfitrión del servidor web
# address = "localhost"
address = "192.168.100.46"
# address = "192.168.1.254"
# Puerto en el cual el servidor estará atendiendo solicitudes HTTP
# El default de un servidor web en produción debe ser 80
port = 80


class WebServer(BaseHTTPRequestHandler):
	"""Sirve cualquier archivo encontrado en el servidor"""
	def _serve_file(self, rel_path):
		if not os.path.isfile(rel_path):
			self.send_error(404)
			return
		self.send_response(200)
		mime = magic.Magic(mime=True)
		self.send_header("Content-type", mime.from_file(rel_path))
		self.end_headers()
		with open(rel_path, 'rb') as file:
			self.wfile.write(file.read())


	"""Sirve el archivo de interfaz de usuario"""
	def _serve_ui_file(self):
		if not os.path.isfile("user_interface.html"):
			err = "user_interface.html not found."
			self.wfile.write(bytes(err, "utf-8"))
			print(err)
			return
		try:
			with open("user_interface.html", "r") as f:
				content = "\n".join(f.readlines())
		except:
			content = "Error reading user_interface.html"
		self.wfile.write(bytes(content, "utf-8"))

	def _parse_post(self, json_obj):
		if not 'action' in json_obj or not 'value' in json_obj:
			return
			


	"""do_GET controla todas las solicitudes recibidas vía GET, es
	decir, páginas. Por seguridad, no se analizan variables que lleguen
	por esta vía"""
	def do_GET(self):
		# Revisamos si se accede a la raiz.
		# En ese caso se responde con la interfaz por defecto
		if self.path == '/':
			# 200 es el código de respuesta satisfactorio (OK)
			# de una solicitud
			self.send_response(200)
			# La cabecera HTTP siempre debe contener el tipo de datos mime
			# del contenido con el que responde el servidor
			self.send_header("Content-type", "text/html")
			self.send_header("Access-Control-Allow-Origin", "*")
			# Fin de cabecera
			self.end_headers()
			# Por simplicidad, se devuelve como respuesta el contenido del
			# archivo html con el código de la página de interfaz de usuario
			self._serve_ui_file()
		# En caso contrario, se verifica que el archivo exista y se sirve
		elif self.path == '/read':
			self.send_response(200)
			
			self.send_header("Content-type", "application/json")
			self.send_header("Access-Control-Allow-Origin", "*")
			self.end_headers()

			data = readNLectures()
			json_response = json.dumps(data)
			self.wfile.write(json_response.encode('utf-8'))
		else:
			self._serve_file(self.path[1:])


	"""do_POST controla todas las solicitudes recibidas vía POST, es
	decir, envíos de formulario. Aquí se gestionan los comandos para
	la Raspberry Pi"""
	def do_POST(self):
		# Primero se obtiene la longitud de la cadena de datos recibida
		content_length = int(self.headers.get('Content-Length'))
		if content_length < 1:
			return
		# Después se lee toda la cadena de datos
		post_data = self.rfile.read(content_length)
		# Finalmente, se decodifica el objeto JSON y se procesan los datos.
		# Se descartan cadenas de datos mal formados
		try:
			jobj = json.loads(post_data.decode("utf-8"))
			self._parse_post(jobj)
		except:
			print(sys.exc_info())
			print("Datos POST no recnocidos")

def main():
	# Inicializa una nueva instancia de HTTPServer con el
	# HTTPRequestHandler definido en este archivo
	webServer = HTTPServer((address, port), WebServer)
	print("Servidor iniciado")
	print ("\tAtendiendo solicitudes en http://{}:{}".format(
		address, port))

	try:
		# Mantiene al servidor web ejecutándose en segundo plano
		webServer.serve_forever()
	except:
		print(sys.exc_info())
	webServer.server_close()
	# Reporta parada del servidor web en consola
	print("Server stopped.")


# Punto de anclaje de la función main
if __name__ == "__main__":
  tempThread = threading.Thread(target=readTempFromSlave)
  tempThread.start()
  main()
  print("Fin del programa...")


