ip link set can0 type can bitrate 250000 loopback on
ifconfig can0 txqueuelen 10000
ifconfig can0 up