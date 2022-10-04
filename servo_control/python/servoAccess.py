import serial

# will later implement a code to find and connect to serial ports

ser = serial.Serial('/dev/ttyUSB2', 115200) # '/dev/ttyUSB0' on linux
#res = ser.read()
#print(res)


# packet to make LED green
header = 0xFF
packetSize = 0x0A # 10
pID = 0x02
cmd = 0x03

data0 = 0x35 # 53
data1 = 0x01
data2 = 0x01

checkSum1 = 0xC0 #(packetSize ^ pID ^ cmd ^ data0 ^ data1) and 0xFE
checkSum2 = 0x3E #(~checkSum1) and 0xFE

ser.write(header)
ser.write(packetSize)
ser.write(pID)
ser.write(cmd)
ser.write(checkSum1)
ser.write(checkSum2)
ser.write(data0)
ser.write(data1)
ser.write(data2)

ser.close()
