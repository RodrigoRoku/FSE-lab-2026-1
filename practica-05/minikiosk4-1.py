
import vlc
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

instance = vlc.Instance()
media_list = instance.media_list_new()

files = [
  '/home/pi/videos/video.mp4',
	'/home/pi/pictures/pic01.jpg',
	'/home/pi/pictures/pic02.jpg',
	'/home/pi/pictures/pic03.jpg',
	'/home/pi/pictures/pic04.jpg'
]

for file in files:
  media_list.add_media(instance.media_new(file)) 
media_list_player = instance.media_list_player_new()
media_list_player.set_media_list(media_list)
#Para modular volumen
player = media_list_player.get_media_player()
continueLoop = True
currentVolume = 50


def playMedia():
  #Reproducir el video por 20 segundos, probar funciones de volumen
  global continueLoop
  media_list_player.play() #Reproduce el video
  player.audio_set_volume(currentVolume)
  sleep(20)
  #Eliminar el video de la lista para que no se siga repitiendo
  media_list.lock()
  media_list.remove_index(0)
  media_list.unlock()
  #Reproducir imàgenes en loop infinito, probar pause, next 
  while continueLoop:
    if player.is_playing() != 0:
      media_list_player.next()
      sleep(3)
      
#se usa la numeraciòn de los pines
botones = [3, 5, 7, 11, 13, 15]
for boton in botones:
  GPIO.setup(boton, GPIO.IN)


def anterior(channel):
  print("imagen Anterior")
  media_list_player.previous()
  

def siguiente(channel):
  print("imagen siguiente")
  media_list_player.next()
  

def parar(channel):
  global continueLoop
  print("Parar")
  continueLoop = False
  media_list_player.stop()
  GPIO.cleanup()
  
def pausar(channel):
  media_list_player.pause()
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
