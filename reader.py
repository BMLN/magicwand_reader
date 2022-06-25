import os
import serial



monitor = serial.Serial(port=os.environ["ARD_PORT"], baudrate=os.environ["ARD_BAUD"], timeout=.1)

x = 0
while True and x < 20:
    print(monitor.readline())
    x += 1

monitor.close()


exit()