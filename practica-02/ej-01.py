# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/2025

from machine import Pin     
from utime import sleep_ms  

led = Pin(25, Pin.OUT)      

while(True):                # Repeat forever
    led.on()            
    sleep_ms(1)
    led.off()
    sleep_ms(5)
