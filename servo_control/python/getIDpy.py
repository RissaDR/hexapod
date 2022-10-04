import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 115200) # '/dev/ttyUSB0' on linux

def serRead():
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
    print(data[i])
    ser.write(bytes([data[i]]))
    i += 1
  serRead()

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
    print("sent", i, data[i])
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
  #serRead()


nid = 0xFE
#clearError()
#changeIDEEPx(nid)
print(statxgetid(24))


