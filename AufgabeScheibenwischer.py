#!/usr/bin/python
# coding=utf-8

import RPi.GPIO as GPIO
import Adafruit_DHT
import time
 
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM) 
 
# Hier kann der Pin deklariert werden, an dem das Sensormodul angeschlossen ist
GPIO_Pin = 17
#motor gpio pins
GPIO_4 = 26 
GPIO_3 = 19
GPIO_2 = 13
GPIO_1 = 6

GPIO.setup(GPIO_1, GPIO.OUT)
GPIO.setup(GPIO_2, GPIO.OUT)
GPIO.setup(GPIO_3, GPIO.OUT)
GPIO.setup(GPIO_4, GPIO.OUT)
 
print('KY-015 Sensortest - Temperatur und Luftfeuchtigkeit')

base, temp = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)

def motor(sleeptime):
	for x in range(5):
		GPIO.output(GPIO_1, GPIO.HIGH)
		GPIO.output(GPIO_2, GPIO.LOW)
		GPIO.output(GPIO_3, GPIO.LOW)
		GPIO.output(GPIO_4, GPIO.HIGH)
		time.sleep(sleeptime)
		GPIO.output(GPIO_1, GPIO.LOW)
		GPIO.output(GPIO_2, GPIO.HIGH)
		GPIO.output(GPIO_3, GPIO.HIGH)
		GPIO.output(GPIO_4, GPIO.LOW)
		time.sleep(sleeptime)
	for x in range(5):
		GPIO.output(GPIO_1, GPIO.HIGH)
		GPIO.output(GPIO_2, GPIO.LOW)
		GPIO.output(GPIO_3, GPIO.HIGH)
		GPIO.output(GPIO_4, GPIO.LOW)
		time.sleep(sleeptime)
		GPIO.output(GPIO_1, GPIO.LOW)
		GPIO.output(GPIO_2, GPIO.HIGH)
		GPIO.output(GPIO_3, GPIO.LOW)
		GPIO.output(GPIO_4, GPIO.HIGH)
		time.sleep(sleeptime)

try:
    while(True):
			# Messung wird gestartet und das Ergebnis in die entsprechenden Variablen geschrieben
			Luftfeuchte, Temperatur = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
 
			print("-----------------------------------------------------------------")
			if Luftfeuchte is not None and Temperatur is not None:
 
				# Das gemessene Ergebnis wird in der Konsole ausgegeben
				print('Temperatur = {0:0.1f}°C  | rel. Luftfeuchtigkeit = {1:0.1f}%'.format(Temperatur, Luftfeuchte))
			# Da der Raspberry Pi aufgrund des Linux-Betriebsystems für Echtzeitanwendungen benachteiligt ist,
			# kann es sein, dass aufgrund von Timing Problemen die Kommunikation scheitern kann.
			# In dem Falle wird eine Fehlermeldung ausgegeben - ein Ergebnis sollte beim nächsten Versuch vorliegen
			else:
				print('Fehler beim Auslesen - Bitte warten auf nächsten Versuch!')
			print("-----------------------------------------------------------------")
			
			if Luftfeuchte > 35:
				motor(0.4)
			if Luftfeuchte > 50:
				motor(0.2)
			if Luftfeuchte > 70:
				motor(0.1)
			if Luftfeuchte > 90:
				motor(0.05)
			
			
					
				
 
			
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()
 