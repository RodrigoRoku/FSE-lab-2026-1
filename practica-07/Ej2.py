import lcdManager
import sensor
from time import sleep

nombre = "Tapia Navarro Hernandez Alejo"
index = 0 

def formNextPrintableWord():
  global index
  i = index
  printable = ""
  for char in range(16):
    if(i >= len(nombre)):
      i = 0
    printable += nombre[i]
    i += 1
    
  index = index + 1 
  if(index >= len(nombre)):
    index = 0
  
  return printable

lcd = lcdManager.lcdManager()
try:
  tempSensor = sensor.temperatureSensor()
except:
  print(e)


try:
  while True:
    data = tempSensor.readTemp()
    printable = formNextPrintableWord()
    lcd.sendCommand(0x01)
    sleep(0.005)
    lcd.setPosition(0,0)
    lcd.printWord(printable)
    lcd.setPosition(1,0)
    lcd.printWord("{} C {} F".format(data.get('temp_c'), data.get('temp_f')))
    sleep(1)
except Exception as e:
  print(e)
