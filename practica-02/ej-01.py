# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/2025

from machine import Pin     
from utime import sleep_ms  

led = Pin(25, Pin.OUT)      

def blink(timer): # Callback function
    led.on()
    sleep_ms(1)
    led.off()
    sleep_ms(20)

timer = Timer() # Create the Timer object
timer.init(freq=10000, # Timer frequency set to 2.5Hz
    mode=Timer.PERIODIC, # Timer will run endlessly (not one-shot)
    callback=blink # Set callback function: blink
)
