import can
import time
from gpiozero import MCP3008, InputDevice
import board
import neopixel

pot = MCP3008(0)
ignition = InputDevice(23, pull_up=False)

bus = can.interface.Bus(channel="can0", bustype="socketcan")
pixels = neopixel.NeoPixel(board.D18, 8, brightness=1)
speed = 0
rpm = 800


def construct_j1939_can_id(priority, pgn, sa, dp=0):
    can_id = (priority << 26) | (pgn << 8) | sa | (dp << 7)
    return can_id


def set_rpm(value):
    priority = 6
    pgn_for_rpm = 61444
    sa = 0
    #rpm_in_hex = int(hex(value), 16)

    j1939_can_id = construct_j1939_can_id(priority, pgn_for_rpm, sa)
    # data = value.to_bytes(2, byteorder='little', signed=False)
    if ignition.value == 1:
        pixels[0] = (255, 0, 0)
        data = [0x00, 0x00, 0x00, 0x80, 0x3E, 0x00, 0x00, 0x00]
    else:
        pixels[0] = (0, 0, 0)
        data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    # can0  18F00400   [8]  00 00 00 B0 04 00 00 00
    msg = can.Message(arbitration_id=j1939_can_id, data=data, is_extended_id=True)
    try:
        bus.send(msg)
        print(f"J1939 CAN message sent successfully with id = {j1939_can_id} data = {data}")
    except can.CanError:
        print("Error sending J1939 CAN message")


def set_speed(value):
    priority = 6
    pgn_for_speed = 65265
    sa = 0
    j1939_can_id = construct_j1939_can_id(priority, pgn_for_speed, sa)
    data = [0x00, 0x00, value, 0x00, 0x00, 0x00, 0x00, 0x00]

    msg = can.Message(arbitration_id=j1939_can_id, data=data, is_extended_id=True)
    try:
        bus.send(msg)
        #print(f"J1939 CAN message sent successfully with id = {j1939_can_id} data = {data}")
    except can.CanError:
        print("Error sending J1939 CAN message")



print("Press CTRL-C to exit.")
try:
    while True:
        print(pot.value)
        speed = int(round(pot.value*100, 2))
        set_speed(speed)
        set_rpm(rpm)
        time.sleep(0.5)
except KeyboardInterrupt:
    pixels[0] = (0, 0, 0)
finally:
    pot.close
    ignition.close        

