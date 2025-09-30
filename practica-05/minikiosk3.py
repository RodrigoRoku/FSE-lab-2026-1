#!/bin/python3
#
# kyosk.py
#
# Author:  Mauricio Matamoros
# Date:    2023.02.14
# License: MIT
#
# Plays a video file using VLC with the Raspberry Pi
#
import vlc
from time import sleep
import  os

player = vlc.MediaPlayer()
video = vlc.Media('/home/ximena/Downloads/FSEm - practica 05/pi/videos/video.mp4')
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

