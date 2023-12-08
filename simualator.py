import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
drive_pin = 16
stop_pin = 36
GPIO.setup(drive_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


import can
import time
from flask import request
import time

bus = can.interface.Bus(channel='can0', bustype='socketcan')

speed = 0
rpm = 800

def construct_j1939_can_id(priority, pgn, sa, dp=0):
    can_id = (priority << 26) | (pgn << 8) | sa | (dp << 7)
    return can_id


def set_rpm(value):
    priority = 6
    pgn_for_rpm = 61444
    sa = 0
    rpm_in_hex = int(hex(value), 16)
    
    j1939_can_id = construct_j1939_can_id(priority, pgn_for_rpm, sa)
    #data = value.to_bytes(2, byteorder='little', signed=False)
    data = [0x00, 0x00, 0x00 , 0x80, 0x3E, 0x00, 0x00, 0x00]
    #can0  18F00400   [8]  00 00 00 B0 04 00 00 00
    msg = can.Message(arbitration_id=j1939_can_id, data=data, is_extended_id=True)
    try:
        bus.send(msg)
        print(f"J1939 CAN message sent successfully with id = {j1939_can_id} data = {data}")
    except can.CanError:
        print("Error sending J1939 CAN message")
    
    

def set_speed(value):
    global speed
    priority = 6
    pgn_for_speed = 65265
    sa = 0
    speed_in_hex = int(hex(value), 16)

    j1939_can_id = construct_j1939_can_id(priority, pgn_for_speed, sa)
    print(speed_in_hex)
    data = [0x00, 0x00, value , 0x00, 0x00, 0x00, 0x00, 0x00]
    
    msg = can.Message(arbitration_id=j1939_can_id, data=data, is_extended_id=True)
    try:
        bus.send(msg)
        print(f"J1939 CAN message sent successfully with id = {j1939_can_id} data = {data}")
    except can.CanError:
        print("Error sending J1939 CAN message")
        

def stop(button):
    global speed
    speed = 0
    global rpm
    rpm = 800
    
def drive(button):
    global speed
    speed = 50
    global rpm
    rpm = 1200
    

GPIO.add_event_detect(drive_pin, GPIO.BOTH, callback=drive, bouncetime=5)
GPIO.add_event_detect(stop_pin, GPIO.BOTH, callback=stop, bouncetime=5)

print("Press CTRL-C to exit.")
try:
    while True:
        set_speed(speed)
        set_rpm(rpm)
        time.sleep(1)
        pass
finally:
    GPIO.cleanup() 

