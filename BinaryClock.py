import RPi.GPIO as GPIO
import time
#using only zip() limits changes to the length of the binary number
#in order to switch LEDs off, the binary string processed needs to be 000101, not 101 for example
from itertools import zip_longest

pmPin       = 22

#I had these pinsets wired in opposite directions (asc and dec). It was easier to change the code than the wires
minutePins  = [12,29,31,33,35,37]
hourPins    = [40,38,36,32]

def setup():
    print ('Programme start...')
    GPIO.setmode(GPIO.BOARD)
    for pin in [pmPin]+[minutePins]+[hourPins]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)


def loop():
    #testing - display begins on the rightmost side - therefore -1 break in the slice is needed
    #each pin is paired with 1 or 0
    print("hour =",time.localtime().tm_hour%12,"=>",bin(time.localtime().tm_hour%12),tuple(zip_longest(hourPins, [int(isOn) for isOn in bin(time.localtime().tm_hour%12)[:1:-1]],fillvalue=0)))
    print("minute =",time.localtime().tm_min,"=>",bin(time.localtime().tm_min),tuple(zip_longest(minutePins,[int(isOn) for isOn in bin(time.localtime().tm_min)[:1:-1]],fillvalue=0)))
    while True:
        

        #set AM/PM LED
        GPIO.output(pmPin, GPIO.HIGH) if time.localtime().tm_hour<=12 else GPIO.output(pmPin, GPIO.LOW)

        #set hour LEDs
        for isOn,led in tuple(zip([int(isOn) for isOn in bin(time.localtime().tm_hour%12)[:1:-1]],hourPins)):
            GPIO.output(led, GPIO.LOW if isOn else GPIO.HIGH)

        #set minute LEDs
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
