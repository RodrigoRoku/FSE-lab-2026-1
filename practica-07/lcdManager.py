import smbus2
from time import sleep

I2C_ADDRESS = 0x27
LINE_WIDTH = 16
ENABLE = 0x04

#algunos comandos para inicializacion
INIT_DISPLAY = 0X33
MODE_4_BIT = 0X32
MODE_2_LINES = 0X28
ENABLE_HIDE_CURSOR = 0X0C # 0000 0 1 Display on/off cursor on/off Blink on/off
CLEAR_SCREEN = 0X01
BL_ENABLE = 0X08

LCD_INITIAL_POSITION = 0X80

def sleep_ms(miliseconds):
  sleep(float(miliseconds/1000))

class lcdManager:
  
  def __init__(self):
    self.bus = smbus2.SMBus(1)
    self.startDisplay()
    self.setPosition(0,0)
  
  def sendCommand(self, cmd):
    bufferHigh = (cmd & 0xF0) | ENABLE
    bufferLow = ((cmd  & 0x0F) << 4) | ENABLE
    
    self.bus.write_byte(I2C_ADDRESS, bufferHigh)
    sleep_ms(2)
    #cambia bandera enable
    bufferHigh = bufferHigh & ~ENABLE
    self.bus.write_byte(I2C_ADDRESS, bufferHigh)
    sleep_ms(2)

    self.bus.write_byte(I2C_ADDRESS, bufferLow )
    sleep_ms(2)
    bufferLow = bufferLow & ~ENABLE
    self.bus.write_byte(I2C_ADDRESS, bufferLow)
    sleep_ms(2)
  
  def startDisplay(self):
    self.sendCommand(INIT_DISPLAY)
    sleep_ms(5)
    self.sendCommand(MODE_4_BIT)
    sleep_ms(5)
    self.sendCommand(ENABLE_HIDE_CURSOR)
    sleep_ms(5)
    self.sendCommand(MODE_2_LINES)
    sleep_ms(5)
    self.sendCommand(CLEAR_SCREEN)
    sleep_ms(5)
  
  def sendData(self, data):
    bufferHigh = (data & 0xF0) | 0x01  | BL_ENABLE | ENABLE
    bufferLow = ((data  & 0x0F) << 4) | 0x01  | BL_ENABLE | ENABLE
      
    self.bus.write_byte(I2C_ADDRESS, bufferHigh )
    sleep_ms(2)
    #cambia bandera enable 1111 1011
    bufferHigh = bufferHigh & ~ENABLE
    self.bus.write_byte(I2C_ADDRESS, bufferHigh)
    sleep_ms(2)
    
    self.bus.write_byte(I2C_ADDRESS, bufferLow)
    sleep_ms(2)
    bufferLow = bufferLow & ~ENABLE
    self.bus.write_byte(I2C_ADDRESS, bufferLow)
    sleep_ms(2)
  
  def printWord(self, word):
    for char in word:
      self.sendData(ord(char))
  
  def setPosition(self, line, pos):
    
    position  = LCD_INITIAL_POSITION + (0x40 * line) + pos 
    self.sendCommand(position)

# manager = lcdManager()
# manager.setPosition(0,0)
# manager.printWord("Tapia")
# manager.printWord("Temperatura = ºC")
# sleep(3)
# manager.sendCommand(0x01)
# sleep_ms(2) #Sin el delay el LCD se comporta extraño
# manager.setPosition(0,0)
# manager.printWord("Hola Mundo ")
# manager.setPosition(1,2)
# manager.printWord("Temperatura = ºC")

