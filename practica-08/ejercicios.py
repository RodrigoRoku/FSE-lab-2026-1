import lcdManager
import utils
from time import sleep
lcd = lcdManager.lcdManager()

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
  

ejercicio1()
sleep(2)
ejercicio2()
