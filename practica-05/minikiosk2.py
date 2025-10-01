#!/bin/python3
#
# minikiosk.py
#
# # Autor: Tapia Navarro Rodrigo y Hernández Alejo Ximena Gizell
# Date:    2025.09.23
#
# Reproduce un video na serie de imagenes en bucle de una carpeta predetermindada.
# Cuando detecta una USB reproduce las imàgenes de la USB usando VLC.
#

import vlc
import os
import pyudev
from time import sleep
import threading 
import subprocess as sp

swapPlaylist = False
currentPlaylist = None
externalImages = []


player = vlc.MediaPlayer()
#player.set_fullscreen(True)
defaulFiles = [
	'/home/pi/pictures/pic01.jpg',
	'/home/pi/pictures/pic02.jpg',
	'/home/pi/pictures/pic03.jpg',
	'/home/pi/pictures/pic04.jpg'
]

defaultImagenes = []
for file in defaulFiles:
	defaultImagenes.append(vlc.Media(file))
currentPlaylist = defaultImagenes

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")

def show_images():
	player = vlc.MediaPlayer()
	video = vlc.Media('/home/pi/videos/video.mp4')
	player.set_media(video)
	player.play()
	sleep(10)
	i=0
	global swapPlaylist
	while True:
		if swapPlaylist:
			i = 0 
			swapPlaylist = False 
		player.set_media(currentPlaylist[i])
		player.play()
		sleep(3)
		i = i + 1
		if i >= len(currentPlaylist):
			i = 0

def get_photos_device(path):
	photos = []
	for file in os.listdir(path):
		if file.endswith(".jpg") \
		or file.endswith(".png") or file.endswith(".jpeg"):
			photos.append(vlc.Media(path +'/'+ file))
	return photos
#end def


def auto_mount(path):
	args = ["udisksctl", "mount", "-b", path]
	sp.run(args)
#end def

def get_mount_point(path):
	args = ["findmnt", "-unl", "-S", path]
	cp = sp.run(args, capture_output=True, text=True)
	out = cp.stdout.split(" ")[0]
	return out
#end def

def monitor_devices():
	global swapPlaylist
	global currentPlaylist
	global defaultImagenes
	while True:
		action, device = monitor.receive_device()
		if action == "add":	
			auto_mount("/dev/" + device.sys_name)		
			mp = get_mount_point("/dev/" + device.sys_name)
			externalImages = get_photos_device(mp)
			currentPlaylist = externalImages
			swapPlaylist = True	
			print(currentPlaylist)
		elif action == "remove":
			print("Se elimino el dispositivo")
			currentPlaylist = defaultImagenes
			swapPlaylist = True	
			print(currentPlaylist)


usbDetectorThread = threading.Thread(target=monitor_devices)
mediaPlayerThread = threading.Thread(target=show_images)

usbDetectorThread.start()
mediaPlayerThread.start()

usbDetectorThread.join()
mediaPlayerThread.join()

