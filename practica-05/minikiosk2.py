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
#GIzell dice que lo hagamos con hilos ñiñiñi
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
# defaulFiles = [
# 	'/home/pi/pictures/pic01.jpg',
# 	'/home/pi/pictures/pic02.jpg',
# 	'/home/pi/pictures/pic03.jpg',
# 	'/home/pi/pictures/pic04.jpg'
# ]
defaulFiles = [
	'/home/rodrigo/Pictures/prueba/pic01.jpg',
	'/home/rodrigo/Pictures/prueba/pic02.jpg',
	'/home/rodrigo/Pictures/prueba/pic03.jpg',
	'/home/rodrigo/Pictures/prueba/pic04.jpg'
]
defaultImagenes = []
for file in defaulFiles:
	defaultImagenes.append(vlc.Media(file))
currentPlaylist = defaultImagenes

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")

def show_images():
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

