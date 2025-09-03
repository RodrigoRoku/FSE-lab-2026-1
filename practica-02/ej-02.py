# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/2025

from machine import ADC          
from utime import sleep_ms       

def main(): # Main function
    K = -0.029259019 # Conversion factor
    adc = machine.ADC(4) # Init ADC on pin 4
    while(True): # Repeat forever
        x = adc.read_u16() # Read ADC
        temp = x * K + 437.23 # Convert to celcius
        temp_F = temp *1.8 + 32
        print(f'Temp: {temp}°C') # Print temperature
        print(f'Temp: {temp_F}°F') # Print temperature
        sleep_ms(1000) # Wait for 1000ms
#end def

if __name__ == '__main__':
    main()
