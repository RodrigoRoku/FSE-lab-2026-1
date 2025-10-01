#!/bin/python3
#
# minikiosk.py
#
# # Autor: Tapia Navarro Rodrigo y Hernández Alejo Ximena Gizell
# Date:    2025.09.23
#
# Reproduce un video durante 10 segundos luego una serie de imagenes en bucle usando VLC.
#

import vlc
from time import sleep

player = vlc.MediaPlayer()
video = vlc.Media('/home/pi/videos/video.mp4')
files = [
	'/home/pi/pictures/pic01.jpg',
	'/home/pi/pictures/pic02.jpg',
	'/home/pi/pictures/pic03.jpg',
	'/home/pi/pictures/pic04.jpg'
]
i= 0
imagenes = []
for file in files:
	imagenes.append(vlc.Media(file))

player.set_media(video)
player.play()
sleep(10)
i=0
while True:
	player.set_media(imagenes[i])
	player.play()
	sleep(3)
	i = i + 1
	if i >= len(imagenes):
		i = 0

	

