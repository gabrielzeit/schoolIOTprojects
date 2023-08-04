import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

Trigger_AusgangsPin = 38
Echo_EingangsPin    = 40
 
# Die Pause zwischen den einzelnen Messugnen kann hier in Sekunden eingestellt werden
sleeptime = 0.8
 
# Hier werden die Ein-/Ausgangspins konfiguriert
GPIO.setup(Trigger_AusgangsPin, GPIO.OUT)
GPIO.setup(Echo_EingangsPin, GPIO.IN)
GPIO.output(Trigger_AusgangsPin, False)
 
# Hauptprogrammschleife
try:
    while True:
        # Abstandsmessung wird mittels des 10us langen Triggersignals gestartet
        GPIO.output(Trigger_AusgangsPin, True)
        time.sleep(0.00001)
        GPIO.output(Trigger_AusgangsPin, False)
 
        # Hier wird die Stopuhr gestartet
        EinschaltZeit = time.time()
        while GPIO.input(Echo_EingangsPin) == 0:
            EinschaltZeit = time.time() # Es wird solange die aktuelle Zeit gespeichert, bis das Signal aktiviert wird
 
        while GPIO.input(Echo_EingangsPin) == 1:
            AusschaltZeit = time.time() # Es wird die letzte Zeit aufgenommen, wo noch das Signal aktiv war
 
        # Die Differenz der beiden Zeiten ergibt die gesuchte Dauer
        Dauer = AusschaltZeit - EinschaltZeit
        # Mittels dieser kann nun der Abstand auf Basis der Schallgeschwindigkeit der Abstand berechnet werden
        Abstand = (Dauer * 34300) / 2
 
        
        if Abstand < 2 or (round(Abstand) > 300):
            print("------------------------------")
        else:
            
            Abstand = format((Dauer * 34300) / 2, '.2f')
          
            print("------------------------------"), Abstand , ("cm")
 
        # Pause zwischen den einzelnen Messungen
        time.sleep(sleeptime)
 
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()