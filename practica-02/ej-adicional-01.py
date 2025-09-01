# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/2025

from machine import Pin
from machine import PWM

led = Pin(25, Pin.OUT)

max_duty = 65535

led_pwm = PWM(led, freq = 200);

duty_cycle = 100

led_pwm.duty_u16(int((max_duty * duty_cycle)/100)) #Ciclo de trabajo del 50%

duty = led_pwm.duty_u16()

print(f'duty: \t {duty}') 
