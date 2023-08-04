# Benoetigte Module werden importiert und eingerichtet
import RPi.GPIO as GPIO
import time
   
GPIO.setmode(GPIO.BCM)
   
lichtAktiv = False
erschAktiv = False
erschAktiv2 = False
gesamtErsch = False
neigungAktiv = False
kindersitzAktiv = False



# Hier wird der Eingangs-Pin deklariert, an dem der Sensor angeschlossen ist. Zusaetzlich wird auch der PullUP Widerstand am Eingang aktiviert
#Lichtschranken
GPIO_PIN_L = 22
GPIO.setup(GPIO_PIN_L, GPIO.IN)
#Erschutterungssensor
GPIO_PIN_E = 2
GPIO.setup(GPIO_PIN_E, GPIO.IN)
#Neigungssensor
GPIO_PIN_N = 13
GPIO.setup(GPIO_PIN_N, GPIO.IN)
#Erschutterungssensor
GPIO_PIN_E2 = 21
GPIO.setup(GPIO_PIN_E2, GPIO.IN)
#KindersitzButton
GPIO_PIN_KB = 12
GPIO.setup(GPIO_PIN_KB, GPIO.IN, pull_up_down = GPIO.PUD_UP)


RELAIS_PIN = 3
GPIO.setup(RELAIS_PIN, GPIO.OUT)
GPIO.output(RELAIS_PIN, False)


delayTime = 1

   
print "Sensor-Test [druecken Sie STRG+C, um den Test zu beenden]"
   

def ausgabeErschutterung(null):
			global startErsch1

			startErsch1 = time.time()

			#print("Erschutterung erkannt")					
			global erschAktiv
			erschAktiv = True
			gesamtErschutterung()
			

def ausgabeErschutterung2(null):
			global startErsch2

			startErsch2 = time.time()
	
			#print("Erschutterung2 erkannt")
			global erschAktiv2
			erschAktiv2 = True
			gesamtErschutterung()
			
			
			
			
def gesamtErschutterung():
			global endErsch
			
			global startErsch1
			global startErsch2
			
			if erschAktiv == True and  erschAktiv2 == True:
					#print("Gesamterschutterung erkannt")
					endErsch = time.time()
					
					
					dif1 = endErsch - startErsch1
					dif2 = endErsch - startErsch2
					
					if dif1 <= 0.5 and dif2 <= 0.5:
						global gesamtErsch
						global erschAktiv
						global erschAktiv2
						gesamtErsch = True
						erschAktiv = False
						erschAktiv2 = False
						print("GESAMTERSCHUTTERUNG")
						startErsch1 = 0
						startErsch2 = 0
						endErsch = 0
					else:
						print("NICHT GESAMTERSCHUTTERUNG")
					
					
		
		
def ausgabeNeigung(null):
			#print("Neigung erkannt")
			global neigungAktiv
			neigungAktiv = True
		
def ausgabeLichtschranken(null):
			print("Lichtschranken erkannt")
			global lichtAktiv
			
			if lichtAktiv == False:
				lichtAktiv = True
			else:
				lichtAktiv = False
				
				
def kindersitzButton(null):
			global kindersitzAktiv
			if kindersitzAktiv == False:
				kindersitzAktiv = True
			else:
				kindersitzAktiv = False
				
			#print("Kindersitz gedruckt")
   
GPIO.add_event_detect(GPIO_PIN_E, GPIO.FALLING, callback=ausgabeErschutterung, bouncetime=100) 
GPIO.add_event_detect(GPIO_PIN_E2, GPIO.FALLING, callback=ausgabeErschutterung2, bouncetime=100) 
GPIO.add_event_detect(GPIO_PIN_N, GPIO.FALLING, callback=ausgabeNeigung, bouncetime=100) 
GPIO.add_event_detect(GPIO_PIN_L, GPIO.FALLING, callback=ausgabeLichtschranken, bouncetime=100) 
GPIO.add_event_detect(GPIO_PIN_KB, GPIO.FALLING, callback=kindersitzButton, bouncetime=100) 
 
 
# Hauptprogrammschleife
try:
        while True:
				time.sleep(1)
				
				
				print("")
				print("RUNDENBEGINN--------------------")
				print("")
				
			
				if neigungAktiv == True:
					if lichtAktiv == False and kindersitzAktiv == False:
						GPIO.output(RELAIS_PIN, True) # NO ist nun kurzgeschlossen
						time.sleep(delayTime)
						GPIO.output(RELAIS_PIN, False) # NC ist nun kurzgeschlossen
						time.sleep(delayTime)
						neigungAktiv = False
						print("Straffen NEIGUNG")
					else:
						print("Nicht straffen NEIGUNG INNEN")
				else:
					print("Nicht straffen NEIGUNG")
				
				
				
			
				if gesamtErsch == True:
					if lichtAktiv == False and kindersitzAktiv == False:
						GPIO.output(RELAIS_PIN, True) # NO ist nun kurzgeschlossen
						time.sleep(delayTime)
						GPIO.output(RELAIS_PIN, False) # NC ist nun kurzgeschlossen
						time.sleep(delayTime)
						gesamtErsch = False
						print("Straffen ERSCHUTTERUNG")
				else:
					print("Nicht straffen ERSCHUTTERUNG")
					
					
				
				
				
   
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
        GPIO.cleanup()