# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/2025

from machine import ADC          
from utime import sleep_ms       

def main():                      
    K = -0.029259019             
    adc = machine.ADC(4)         
    while(True):                 
        x = adc.read_u16()       
        temp = x * K + 437.23 
        temp_farenheit = temp * 1.8 + 32 
        print(f'Temp: {temp_farenheit}°F \t {temp}°C') 
        sleep_ms(1000)           
#end def

if __name__ == '__main__':
    main()
