# Autores:  Rodrigo Tapia Navarro y Gizell Hernàndez Alejo
# Fecha de creaciòn: 25/08/2025

from machine import Pin
from machine import PWM

from machine import Pin # Board IO Pin
from machine import Timer # Hardware timer

led = Pin(25, Pin.OUT) # Setup pin 25 (sentinel LED) as output
led_pwm = PWM(led)
duty_step = 129

led_pwm.freq (5000)
led_pwm.duty_u16(65000)


for duty_cycle in range(65536, 0, -duty_step):
    led_pwm.duty_u16(duty_cycle)
    sleep_ms(5)

