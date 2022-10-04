import serial

ser = serial.Serial('/dev/ttyUSB0', 115200) # '/dev/ttyUSB0' on linux

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
    serread = ser.read()
    if (n == 3):
      returnId = int.from_bytes(serread, "big")
    #print(n, serread.hex())
    print(n, bin(int(serread.hex(), base=16)), "\t", serread.hex())
    n += 1
  
  return returnId

print(statx(0xFE))