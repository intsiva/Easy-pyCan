from gpiozero import MCP3008, InputDevice
from time import sleep


pot = MCP3008(0)
ignition = InputDevice(23, pull_up=False)

while True:
    pot_value = round(pot.value, 2)
    print(pot_value)
    if ignition and pot_value < 1.0:
        print(pot_value)
    print("Ignition = " + str(ignition.value))
    sleep(0.1)