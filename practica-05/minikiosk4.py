
import vlc
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

player = vlc.MediaPlayer()
imagenes = []
files = [
	'/home/pi/pictures/pic01.jpg',
	'/home/pi/pictures/pic02.jpg',
	'/home/pi/pictures/pic03.jpg',
	'/home/pi/pictures/pic04.jpg'
]

for file in files:
  imagenes.append(vlc.Media(file)) 
continueLoop = True
currentVolume = 50
i=0
released = True


def playMedia():
  video = vlc.Media('/home/pi/videos/video.mp4')
  #Reproducir el video por 20 segundos, probar funciones de volumen
  global continueLoop
  player.set_media(video)
  player.play()
  sleep(0.2)
  player.audio_set_volume(currentVolume)
  sleep(20)
  #Reproducir imàgenes en loop infinito, probar pause, next 
  global i
  global released
  player.set_media(imagenes[i])
  player.play()
  while continueLoop:
    if player.is_playing() != 0 and released:
      player.set_media(imagenes[i])
      player.play()
      sleep(5)
      i = i + 1
      if i >= len(imagenes):
        i = 0

#se usa la numeraciòn de los pines
botones = [3, 5, 7, 11, 13, 15]
for boton in botones:
  GPIO.setup(boton, GPIO.IN)


def anterior(channel):
  global i
  global released
  print("imagen Anterior")
  i = i - 1
  if i < 0:
    i= len(imagenes) - 1
  released = False
  player.set_media(imagenes[i])
  player.play()
  sleep(1)
  released = True
  

def siguiente(channel):
  global i
  global released
  print("imagen siguiente")
  i = i + 1
  if i >= len(imagenes):
    i= 0
  released = False
  player.set_media(imagenes[i])
  player.play()
  sleep(1)
  released = True

def parar(channel):
  global continueLoop
  print("Parar")
  continueLoop = False
  player.stop()
  GPIO.cleanup()
  
def pausar(channel):
  player.pause()
  sleep(0.1)
  print(player.get_state()) 

def volumenUp(channel):
  global currentVolume
  print("subiendo volumen")
  currentVolume = currentVolume + 10
  if currentVolume > 100:
    currentVolume = 100
  player.audio_set_volume(currentVolume)

def volumenDown(channel):
  global currentVolume
  print("bajando volumen")
  currentVolume = currentVolume - 10
  if currentVolume < 0:
    currentVolume = 0
  player.audio_set_volume(currentVolume)

GPIO.add_event_detect(3, GPIO.FALLING, 
        callback=anterior, bouncetime=100)
GPIO.add_event_detect(5, GPIO.FALLING, 
        callback=siguiente, bouncetime=100)
GPIO.add_event_detect(7, GPIO.FALLING, 
        callback=parar, bouncetime=100)
GPIO.add_event_detect(11, GPIO.FALLING, 
        callback=pausar, bouncetime=100)
GPIO.add_event_detect(13, GPIO.FALLING, 
        callback=volumenUp, bouncetime=100)
GPIO.add_event_detect(15, GPIO.FALLING, 
        callback=volumenDown, bouncetime=100)

playMedia()
