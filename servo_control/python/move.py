import serial
from time import sleep

# will later implement a code to find and connect to serial ports
# use matrices + inverse kinematics algorithm
# move servo

ser = serial.Serial('/dev/ttyUSB0', 115200) # '/dev/ttyUSB0' on linux

def turnLED(sid, colour):
  data = [0] * 10
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 10 # length
  data[3] = sid # servo id
  data[4] = 0x03 # CMD id

  data[7] = 0x35 # register
  data[8] = 0x01 # length
  data[9] = colour # value 

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9]) & 0xFE
  print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 10):
    print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

def changeID(sid, newid):
  data = [0] * 10
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 10 # length
  data[3] = sid # servo id
  data[4] = 0x03 # CMD id

  data[7] = 0x00 # register
  data[8] = 0x01 # length
  data[9] = newid # value 

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9]) & 0xFE
  print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 10):
    print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

def clearError():
  data = [0] * 11
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 11 # length
  data[3] = 0xFE # servo id
  data[4] = 0x03 # CMD id

  data[7] = 0x30 # register
  data[8] = 0x02 # length
  data[9] = 0x00 # value 
  data[10] = 0x00 # val

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9]) & 0xFE
  print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 11):
    print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

def torqueOn():
  data = [0] * 10
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 10 # length
  data[3] = 0xFE # servo id
  data[4] = 0x03 # CMD id

  data[7] = 0x34 # register
  data[8] = 0x01 # length
  data[9] = 0x60 # value 

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9]) & 0xFE # checksum1
  data[6] = (~data[5]) & 0xFE # checksum2

  i = 0
  while(i < 10):
    print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

def moveServo(servoId, pos, color):
  lo_pos = pos
  hi_pos = (pos >> 8)
  
  data = [0] * 12
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 12 # length
  data[3] = servoId # servo id
  data[4] = 0x06 # CMD id

  data[7] = 60 # playtime
  data[8] = lo_pos # jog lsb
  data[9] = hi_pos # jog msb
  color = color & 0x03
  data[10] = (color << 2) & (~0x02) # set
  data[11] = servoId # id

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9] ^ data[10] ^ data[11]) & 0xFE # checksum1
  data[6] = (~data[5]) & 0xFE # checksum2

  i = 0
  while(i < 12):
    print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

def moveServoex(servoId, pos, color):
  data = [0] * 12
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 12 # length
  data[3] = servoId # servo id
  data[4] = 0x06 # CMD id

  data[7] = 60 # playtime
  data[8] = 0x40 # jog lsb
  data[9] = 0x01 # jog msb
  color = color & 0x03
  data[10] = 0x0A # set
  data[11] = 0x0A # id

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9] ^ data[10] ^ data[11]) & 0xFE # checksum1
  data[6] = (~data[5]) & 0xFE # checksum2

  i = 0
  while(i < 12):
    print(data[i])
    ser.write(bytes([data[i]]))
    i += 1


nid = 18
#clearError()
torqueOn()
changeID(0xFE, nid)
turnLED(nid, 0x02)
moveServoex(18, 0, 0x04)

