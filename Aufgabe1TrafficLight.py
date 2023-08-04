# Benoetigte Module werden importiert und eingerichtet
import random,time 
import RPi.GPIO as GPIO
   
GPIO.setmode(GPIO.BCM)
  
# Hier werden die Ausgangs-Pin deklariert, an dem die LEDs angeschlossen 
# sind.
LED_Red = 26 
LED_Green = 20 
LED_Blue = 21
LED_WGreen = 16
LED_WRed = 19
Button_signal = 2
phase = 0
   
# Set pins to output mode
GPIO.setup(LED_Red, GPIO.OUT) 
GPIO.setup(LED_Green, GPIO.OUT) 
GPIO.setup(LED_Blue, GPIO.OUT) 
GPIO.setup(LED_WGreen, GPIO.OUT) 
GPIO.setup(LED_WRed, GPIO.OUT) 
GPIO.setup(Button_signal, GPIO.IN, pull_up_down = GPIO.PUD_UP)



def car(color):
	if color == "red":
		GPIO.output(LED_Red, GPIO.HIGH)
		GPIO.output(LED_Green, GPIO.LOW)
		GPIO.output(LED_Blue, GPIO.LOW)
	elif color == "green":
		GPIO.output(LED_Red, GPIO.LOW)
		GPIO.output(LED_Green, GPIO.HIGH)
		GPIO.output(LED_Blue, GPIO.LOW)
	elif color == "blue":
		GPIO.output(LED_Red, GPIO.LOW)
		GPIO.output(LED_Green, GPIO.LOW)
		GPIO.output(LED_Blue, GPIO.HIGH)
	elif color == "yellow": #todo
		GPIO.output(LED_Red, GPIO.HIGH)
		GPIO.output(LED_Green, GPIO.HIGH)
		GPIO.output(LED_Blue, GPIO.LOW)
	else:
		GPIO.output(LED_Red, GPIO.LOW)
		GPIO.output(LED_Green, GPIO.LOW)
		GPIO.output(LED_Blue, GPIO.LOW)
	
def blink_green(light, num):
	if light == "car":
		for i in range(0,num):
			walker("red")
			car(0)
			time.sleep(.5)
			car("green")
			time.sleep(.5)
	elif light == "walker":
		for i in range(0,num):
			car("red")
			walker(0)
			time.sleep(.5)
			walker("green")
			time.sleep(.5)

def walker(color):
	if color == "red":
			GPIO.output(LED_WRed, GPIO.HIGH) 
			GPIO.output(LED_WGreen, GPIO.LOW) 
	elif color == "green":
			GPIO.output(LED_WRed, GPIO.LOW) 
			GPIO.output(LED_WGreen, GPIO.HIGH) 
	else:
			GPIO.output(LED_WRed,GPIO.LOW) 
			GPIO.output(LED_WGreen,GPIO.LOW) 
		

	
	
def ausgabeFunktion(null):
	if(phase == 5):
		cycle()

GPIO.add_event_detect(Button_signal, GPIO.FALLING, callback=ausgabeFunktion, bouncetime=100) 


def cycle():
		global phase
	#car blink walker red phase 0
		phase = 0
		blink_green("car",4)
	#car yellow walker red phase 1
		phase = 1
		car("yellow")
		walker("red")
		time.sleep(2)
	#car red and walker green phase 2
		phase = 2
		car("red")
		walker("green")
		time.sleep(11)
	#walker blink and car red phase 3
		phase = 3
		blink_green("walker",4)
	#walker red and car yellow phase 4
		phase = 4
		walker("red")
		car("yellow")
		time.sleep(2)
	#car green and walker red phase 5
		phase = 5
		car("green")
		walker("red")
		time.sleep(11)
	
 
try:
    while True:
		cycle()
	
		
		
		
		
		
				
   
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
        GPIO.cleanup()
