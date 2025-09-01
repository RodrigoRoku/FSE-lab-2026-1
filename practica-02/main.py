# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/2025

from machine import Pin     # Board IO Pin
from machine import Timer   # Hardware timer

def blink(timer):           # Callback function
    led.toggle()            # Toggle the led
#end def

led = Pin(25, Pin.OUT)      # Setup pin 25 (sentinel LED) as output
timer = Timer()             # Create the Timer object
timer.init(freq=2.5,        # Timer frequency set to 2.5Hz
    mode=Timer.PERIODIC,    # Timer will run endlessly (not one-shot)
    callback=blink          # Set callback function: blink
)
