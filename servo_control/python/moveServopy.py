import serial
from time import sleep
import numpy as np

# will later implement a code to find and connect to serial ports

ser = serial.Serial('/dev/ttyUSB0', 115200) # '/dev/ttyUSB0' on linux

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
    #print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

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
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 10):
    #print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

def changeIDRAM(sid, newid):
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
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 10):
    #print(i, data[i])
    ser.write(bytes([data[i]]))
    i += 1

def clearError():
  data = [0] * 11
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 11 # length
  data[3] = 0xFE # servo id
  data[4] = 0x03 # CMD id

  data[7] = 0x30 # register/address
  data[8] = 0x02 # length
  data[9] = 0x00 # value 
  data[10] = 0x00 # val

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9]) & 0xFE
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 11):
    #print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

def changeIDEEP(sid, newid):
  data = [0] * 10
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 10 # length
  data[3] = sid # servo id
  data[4] = 0x01 # CMD id

  data[7] = 0x06 # register/address
  data[8] = 0x01 # length
  data[9] = newid # value 

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9]) & 0xFE
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 10):
    #print(i, data[i])
    ser.write(bytes([data[i]]))
    i += 1

def changeMin(sid, minpos1, minpos2):
  data = [0] * 11
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 11 # length
  data[3] = sid # servo id
  data[4] = 0x01 # CMD id

  data[7] = 20 # register/address
  data[8] = 0x02 # length
  data[9] = minpos1 # value 
  data[10] = minpos2

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9] ^ data[10]) & 0xFE
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 11):
    #print(i, data[i])
    ser.write(bytes([data[i]]))
    i += 1

def changeMax(sid, maxpos1, maxpos2):
  data = [0] * 11
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 11 # length
  data[3] = sid # servo id
  data[4] = 0x01 # CMD id

  data[7] = 22 # register/address
  data[8] = 0x02 # length
  data[9] = maxpos1 # value 
  data[10] = maxpos2

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9] ^ data[10]) & 0xFE
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 11):
    #print(i, data[i])
    ser.write(bytes([data[i]]))
    i += 1

def statx(sid):
  data = [0] * 7
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 0x07 # length
  data[3] = sid # servo id
  data[4] = 0x07 # CMD id

  data[5] = (data[2] ^ data[3] ^ data[4]) & 0xFE
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 7):
    #print(i, data[i])
    ser.write(bytes([data[i]]))
    i += 1

  while not(ser.inWaiting()):
    pass

  n = 0
  while(ser.inWaiting()):
    #print(bin(int(ser.read().hex(), base=16)))
    print(n, ser.read().hex())
    n += 1

def statxgetid(sid):
  data = [0] * 7
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 0x07 # length
  data[3] = sid # servo id
  data[4] = 0x07 # CMD id

  data[5] = (data[2] ^ data[3] ^ data[4]) & 0xFE
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 7):
    #print(i, data[i])
    ser.write(bytes([data[i]]))
    i += 1

  while not(ser.inWaiting()):
    pass

  n = 0
  while(ser.inWaiting()):
    #print(bin(int(ser.read().hex(), base=16)))
    serread = ser.read()
    if (n == 3):
      returnId = int.from_bytes(serread, "big")
    #print(n, serread.hex())
    print(n, bin(int(serread.hex(), base=16)), "\t", serread.hex())
    n += 1
  
  return returnId

def changeIDEEPx(nid):
  changeIDEEP(statxgetid(0xFE), nid)


def moveServo(servoId, pos, color):
  lo_pos = np.uint8(pos)
  hi_pos = np.uint8((pos >> 8))

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
    #print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

def targetPosition(pos, color):
  moveServo(3, pos, color)
  moveServo(6, pos, color)
  #moveServo(0x01, pos, color)

def posTest(nid, color):
  torqueOn()
  #while(1):
  moveServo(nid, 0, 0x01)
  sleep(1)
  moveServo(nid, 512, 0x02)
  sleep(1)
  moveServo(nid, 1023, 0x01)
  sleep(1)
  moveServo(nid, 512, 0x02)
  sleep(1)

def rollback(sid):
  data = [0] * 9
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 9 # length
  data[3] = sid # servo id
  data[4] = 0x08 # CMD id

  data[7] = 0x00 # id skip
  data[8] = 0x00 # band skip

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8]) & 0xFE
  #print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  #print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 9):
    #print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

cid = 0xFE
#rollback(cid)
torqueOn()
clearError()
#changeIDEEPx(0x03)
#turnLED(cid, 0x04)
posTest(cid, 0x01)
#statxgetid(cid)
#targetPosition(0, 0x01)
print("id", statxgetid(cid))

#look for labels

#working - 3, 5, 6, 7, 17, 19, 20, 24
#driver fault - 12, 2, 11, 8, 15, 13, 18, 21, 26, 28, 23
#odd movement - 16
#cannot move to full range - 4
#could not change id - 9 (not responding to stat)
#no error, not moving (torque on) - 10, 1 (just not moving...)
#garbage detected - 14
#exceed input voltage limit - 22, 27 (vln error)
#? - 25
#will fix drier faults later.








