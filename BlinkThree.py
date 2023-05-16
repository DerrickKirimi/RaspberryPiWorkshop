from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)
led.value(0)

def BlinkThree():
    i =0
    while i<3:
        led.toggle()
        sleep(.3)
        i=i+1
        
while True:
    BlinkThree()
    print("Doing it again")