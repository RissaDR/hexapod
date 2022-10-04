import serial

ser = serial.Serial('/dev/ttyUSB0', 115200) # '/dev/ttyUSB0' on linux

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
  print("checksum1: ", hex(data[5]))
  data[6] = (~data[5]) & 0xFE
  print("checksum2: ", hex(data[6]))

  i = 0
  while(i < 11):
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
    print(data[i])
    ser.write(bytes([data[i]]))
    i += 1

clearError()
turnLED(24, 0x02)