#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import sys

import paho.mqtt.client as mqtt

class Watertank:

  #GPIO Pins zuweisen
  GPIO_TRIGGER = 23
  GPIO_ECHO = 24

  def setup(self):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(Watertank.GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(Watertank.GPIO_ECHO, GPIO.IN)

  def clean(self):
    GPIO.cleanup()

  def measure(self):
    GPIO.output(Watertank.GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(Watertank.GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(Watertank.GPIO_ECHO) == 0:
        StartTime = time.time()

    # speichere Ankunftszeit
    while GPIO.input(Watertank.GPIO_ECHO) == 1:
        StopTime = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopTime - StartTime

    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distance = (TimeElapsed * 34300) / 2

    #print "distance", distance

    #100% = 3.0 0% = 30.0
    level = (30.0 - distance) * (100.0 / 25.0)
    #print "level", level

    return level
