#Programa para leer la temperatura de un sensar DS18B20 utilizando 1-wire
#Los datos del sensor se leen del archivo asociado al sensor
# ubicado en /sys/bus/w1/devices/

from time import sleep
import os

def getFilePath():
    #Directorio en el que se encuentran los dispositivos one wire
    path = '/sys/bus/w1/devices/'
    files = os.listdir(path)
    found = False
    for element in files:
      a = element.find('28')
      if(a != -1):
        path = path + element
        found = True
        break
    if not found:
      raise Exception("No se encontró el directorio para el sensor de temperatura")
    
    path = path + '/w1_slave'
    if not os.path.exists(path):
      raise Exception("No se encontró el archvo para el leer la temperatura")
    
    return path


try:
  temperatureFile = getFilePath()

  while True:
    fp = open(temperatureFile, 'r')
    fileContent = fp.read()
    fp.close()
    position = fileContent.find("t=")
    if position == -1:
      raise Exception("No se encontrò la temperatura en el archivo")
    rawTemp = fileContent[position+2:]
    temperatureCentrigrados = round(float(rawTemp) / 1000,2)
    temperatureFarenheit = round((temperatureCentrigrados * 1.8) + 32.0, 2)
    print("Temperatura = \t {} ºC \t {} ºF".
          format(temperatureCentrigrados, temperatureFarenheit))
    sleep(1)
except Exception as e:
  print(e)