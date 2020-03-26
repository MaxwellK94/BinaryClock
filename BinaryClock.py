import RPi.GPIO as GPIO
import time
pmPin       = 22
#I had these pinsets wired in opposite directions. It was easier to change the code than the wirs.-+
minutePins  = [29,31,33,35,37,12]
hourPins    = [40,38,36,32]

def setup():
	print ('Programme start...')
	GPIO.setmode(GPIO.BOARD)
	for pin in [pmPin]+[minutePins]+[hourPins]:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)



def loop():
    #testing - display begins on the rightmost side - therefore -1 break in the slice is needed
    print("hour =",bin(time.localtime().tm_hour%12),tuple(zip(hourPins, [int(isOn) for isOn in bin(time.localtime().tm_hour%12)[:1:-1]])))
    print("minute =",bin(time.localtime().tm_min),tuple(zip(minutePins,[int(isOn) for isOn in bin(time.localtime().tm_min)[:1:-1]])))
    while True:


        #set AM/PM LED
        GPIO.output(pmPin, GPIO.HIGH) if time.localtime().tm_hour<=12 else GPIO.output(pmPin, GPIO.LOW)

        #set hour LED
        for isOn,led in tuple(zip([int(isOn) for isOn in bin(time.localtime().tm_hour%12)[:1:-1]],hourPins)):
            GPIO.output(led, GPIO.LOW if isOn else GPIO.HIGH)

        #set minute LED
        for isOn,led in tuple(zip([int(isOn) for isOn in bin(time.localtime().tm_min)[:1:-1]],minutePins)):
            GPIO.output(led,GPIO.LOW if isOn else GPIO.HIGH)




def terminate():
	for pin in [pmPin]+[minutePins]+[hourPins]:
		GPIO.output(pin, GPIO.HIGH)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		terminate()