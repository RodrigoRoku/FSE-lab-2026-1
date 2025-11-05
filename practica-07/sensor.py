#Programa para leer la temperatura de un sensar DS18B20 utilizando 1-wire
#Los datos del sensor se leen del archivo asociado al sensor
# ubicado en /sys/bus/w1/devices/

from time import sleep
import os

class temperatureSensor:
  
  def __init__(self):
    self.sensorFile =  '/sys/bus/w1/devices/'
    self.getFilePath()

  def getFilePath(self):
    files = os.listdir(self.sensorFile)
    found = False
    for element in files:
      a = element.find('28')
      if(a != -1):
        self.sensorFile = self.sensorFile + element
        found = True
        break
    if not found:
      raise Exception("No se encontró el directorio para el sensor de temperatura")
    
    self.sensorFile = self.sensorFile + '/w1_slave'
    
    if not os.path.exists(self.sensorFile):
      raise Exception("No se encontró el archvo para el leer la temperatura")
    

  def readTemp(self):
    fp = open(self.sensorFile, 'r')
    fileContent = fp.read()
    fp.close()
    position = fileContent.find("t=")
    if position == -1:
      raise Exception("No se encontrò la temperatura en el archivo")
    rawTemp = fileContent[position+2:]
    temperatureCentrigrados = round(float(rawTemp) / 1000,2)
    temperatureFarenheit = round((temperatureCentrigrados * 1.8) + 32.0, 2)
    return {
      'temp_c': temperatureCentrigrados,
      'temp_f': temperatureFarenheit
    }
    
    

# try:
#   sensor = temperatureSensor()
# except Exception as  e:
#   print(e)

# try:
#   while True:
#     data = sensor.readTemp()
#     print("Temperatura = \t {} ºC \t {} ºF".
#         format(data.get('temp_c'), data.get('temp_f')))
#     sleep(1)
# except Exception as e:
#   print(e)
