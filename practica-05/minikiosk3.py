#!/bin/python3
#
# minikiosk.py
#
# # Autor: Tapia Navarro Rodrigo y Hernández Alejo Ximena Gizell
# Date:    2025.09.23
#
# Reproduce un video 20 segundos, incrementa y decrementa el volumen gradualemte.
#
import vlc
from time import sleep
import  os

player = vlc.MediaPlayer()
video = vlc.Media('/home/pi/videos/video.mp4')
player.set_media(video)
player.play()

def subirV():
        for volumen in range(0, 101, 20):
                player.audio_set_volume(volumen)
                sleep(1)

def bajarV():
        for volumen in range (100, -1, -20):
                player.audio_set_volume(volumen)
                sleep(1)

sleep(0)
subirV()
sleep(10)
bajarV()
player.stop()

