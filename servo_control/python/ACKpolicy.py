import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 115200) # '/dev/ttyUSB0' on linux


# Sets ACK Policy to always reply
# 0: no reply
# 1: reply to READ CMD
# 2: reply to all
# EEP address 7, 1 byte
def ackReply():
  data = [0] * 9
  data[0] = 0xFF # header 1
  data[1] = 0xFF # header 2
  data[2] = 9 # length
  data[3] = 0xFE # servo id
  data[4] = 0x02 # CMD id; EEP write

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