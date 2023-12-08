from gpiozero import MCP3008
from time import sleep
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD)

pot = MCP3008(0)
switch_pin = 16
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ignition = False
def observeIgnition(value):
    global ignition
    ignition = bool(GPIO.input(switch_pin))


GPIO.add_event_detect(switch_pin, GPIO.BOTH, callback=observeIgnition, bouncetime=5)

while True:
    pot_value = round(pot.value, 2)
    if ignition and pot_value < 1.0:
        print(pot_value)
    print("Ignition = " + str(ignition))
    sleep(0.1)