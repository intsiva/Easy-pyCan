# Easy-pyCan

# Dependencies
install python-can

# Setup can port
sudo ip link set can0 type can bitrate 250000

sudo ifconfig can0 up

# Using candump to monitor
sudo candump can0

# Devices used
Raspberry Pi