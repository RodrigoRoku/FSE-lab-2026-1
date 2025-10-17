#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# Autor: Mauricio Matamoros + Modificaciones
# Fecha: Octubre 2025
# ## #############################################################

import smbus2
import struct
import time
import matplotlib.pyplot as plt
import threading

# Dirección I2C del RP2040
SLAVE_ADDR = 0x0A

# Archivo de log
LOG_FILE = './temp.log'

# Inicializar bus I2C (en RPi moderna es bus 1)
i2c = smbus2.SMBus(1)

# Lee la temperatura del sensor conectado por I2C
def readTemperature():
    try:
        msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
        i2c.i2c_rdwr(msg)
        data = list(msg)
        ba = bytearray(data)
        temp = struct.unpack('<f', ba)
        print('Temperatura: {} °C'.format(round(temp[0], 2)))
        return round(temp[0], 2)
    except Exception as e:
        print("Error al leer temperatura:", e)
        return None

# Escribe la temperatura al archivo de log
def log_temp(temperature):
    if temperature is not None:
        try:
            with open(LOG_FILE, 'a') as fp:
                fp.write('{} {}°C\n'.format(
                    time.time(),
                    temperature
                ))
        except Exception as e:
            print("Error al guardar en log:", e)

# Función para graficar en tiempo real
def plot_live():
    plt.figure()
    ax = plt.gca()
    while True:
        try:
            with open(LOG_FILE, 'r') as fp:
                lines = fp.readlines()[-50:]  # Últimos 50 datos
                timestamps, temps = [], []
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        try:
                            timestamps.append(float(parts[0]))
                            temps.append(float(parts[1].replace('°C','')))
                        except:
                            continue
            if temps:
                ax.clear()
                ax.plot(timestamps, temps, 'r-')
                ax.set_title("Temperatura en tiempo real")
                ax.set_xlabel("Tiempo (s)")
                ax.set_ylabel("°C")
                ax.set_ylim(0, 50)
                plt.pause(0.5)
        except Exception as e:
            print("Error en plot:", e)
        time.sleep(1)

# Función principal
def main():
    # Limpiar el archivo de log al iniciar
    try:
        open(LOG_FILE, "w").close()
    except:
        print("Error al limpiar archivo de log.")
        return

    # Lanzar hilo para graficar
    threading.Thread(target=plot_live, daemon=True).start()

    # Bucle principal: leer temp y registrar
    try:
        while True:
            cTemp = readTemperature()
            if cTemp is not None:
                log_temp(cTemp)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario. Saliendo...")

# Entrypoint
if __name__ == '__main__':
    main()
