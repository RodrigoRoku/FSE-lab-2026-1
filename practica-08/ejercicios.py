import lcdManager
import utils
from time import sleep
import sensor

lcd = lcdManager.lcdManager()

try:
  tempSensor = sensor.temperatureSensor()
except:
  print(e)

def ejercicio1():
  lcd.setPosition(0,0)
  lcd.printWord("Rodrigo Tapia ")

def ejercicio2():
  nombre = "Gizell Alejo Rodrigo Tapia "
  while True:
    palabra = utils.formNextPrintableWord(nombre)
    lcd.sendCommand(0x01)
    lcd.printWord(palabra)
    sleep(1)

def ejercicio5():
  nombre = "Gizell Alejo Rodrigo Tapia"
  while True:
    data = tempSensor.readTemp()
    palabra = utils.formNextPrintableWord(nombre)
    lcd.sendCommand(0x01)
    lcd.setPosition(0,0)
    lcd.printWord(palabra)
    lcd.setPosition(1,4)
    temp = f"Temp: {data.get('temp_c')} C"
    lcd.printWord(temp)
    sleep(1)

# ejercicio1()
# sleep(2)
# ejercicio2()
ejercicio5()
