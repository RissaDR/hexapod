import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 115200)

i = 0
#while(1): #!= 2):
i += 1
# ser.write(b"ping")
# ser.write(i)
ser.write(bytes([0x61]))
#ser.write(0xFF)
#print("I sent: ping", i)

while not(ser.inWaiting()):
    pass

while(ser.inWaiting()):
    print(ser.readline())

ser.close()