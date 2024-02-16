from gpiozero import LED, Button, InputDevice 
from signal import pause 
from time import sleep
from gpiozero import GPIOPinInUse

button = InputDevice(23, pull_up=False) 
while True:
    print(button.is_active)
    sleep(0.1)