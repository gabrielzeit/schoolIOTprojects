import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

   
GPIO.setmode(GPIO.BCM)
   
# Hier werden die Ausgangs-Pin deklariert, an dem die LEDs angeschlossen sind.
LED_ROT = 21
LED_GRUEN = 26
LED_BLAU = 20

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

print("HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)
 
GPIO.setup(LED_ROT, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_GRUEN, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_BLAU, GPIO.OUT, initial= GPIO.LOW)

Freq = 100 #Hz

ROT = GPIO.PWM(LED_ROT, Freq) 
GRUEN = GPIO.PWM(LED_GRUEN, Freq)
BLAU = GPIO.PWM(LED_BLAU, Freq)
ROT.start(0)
GRUEN.start(0)
BLAU.start(0)

   
print ("LED-Test [druecken Sie STRG+C, um den Test zu beenden]")


def LED_percentage(percentage):
	ROT.ChangeDutyCycle(percentage)
	GRUEN.ChangeDutyCycle(percentage)
	BLAU.ChangeDutyCycle(percentage)

  
# Hauptprogrammschleife
try:
	while True:
		print(chan0.voltage) 
		LED_percentage(chan0.voltage*100)
		time.sleep(0.05)
   
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
        GPIO.cleanup()