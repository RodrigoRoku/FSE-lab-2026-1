# ## #############################################################
#
# src/pico-code-iic.py
#
# Author: Mauricio Matamoros
#
# Reads temperature from ADC using an LM35 (dummy) and sends
# it via I²C bus
#
# Pro-Tip: rename as main.py in the RP2040
# Pro-Tip: Remove anchor and main functions in i2cslave.py
#
# ## ############################################################
from i2cslave import I2CSlave

from utime import sleep_ms, sleep_us
import ustruct

VAREF          = 3.3
I2C_SLAVE_ADDR = 0x0A


def main():
	setup()
	while True:
		# 1. Get temperature
		temperature = read_avg_temp(10)
		# 2. Convert temperature from pyfloat to bytes
		data = ustruct.pack('<f', temperature)

		# 3. Check if Master requested data
		if i2c.waitForRdReq(timeout=0):
			# If so, send the temperature to Master
			i2c.write(data)
		# end if

		# 3. Check if Master sent data
		if i2c.waitForData(timeout=0):
			# If so, print it
			rcv = i2c.read()
			print( rcv.decode('utf-8') )
		# end if
# end def

def read_avg_temp(count=10):
    '''
        Gets the average of N temperature reads
    '''
    avgtemp = 0
    for i in range(count):
        avgtemp += read_temp()
    return avgtemp / count
# end def
# def read_temp():
# 	# '''Reads temperature in C from the ADC'''
# 	return 25.0
# # end def
def read_temp():
    '''
        Reads temperature in C from the ADC
    '''
    global adcm
    global adcp
    # The actual temperature
    vplus  = adcp.read_u16()
    # The reference temperature value, i.e. 0°C
    vminus = adcm.read_u16()
    # Calculate the difference. when V+ is smaller than V- we have negative temp
    vdiff  = vplus - vminus
    # Now, we need to convert values to the ADC resolution, AKA 3.3V/65536
    # We also know that 1°C = 0.01V so we can multiply by 3.3V / (0.01V/°C) = 330°C
    # to get °C instead of V. Analogously we can multiply VAREF by 100 but
    # since we will divide per 65536, it suffice with dividing by 655.36
    temp = vdiff * VAREF / 655.36
    return temp


def setup():
	global i2c, adcm, adcp
	i2c = I2CSlave(address=I2C_SLAVE_ADDR)
	adcm = machine.ADC(machine.Pin(26))  # Init ADC0
	adcp = machine.ADC(machine.Pin(27))  # Init ADC1
# end def


if __name__ == '__main__':
	main()
