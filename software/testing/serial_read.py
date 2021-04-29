import serial
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
import string
ser = serial.Serial('COM5', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
ser.close()
ser.open()
pcos = [0.1,0.2,0.3,0.4,0.5,0.6]
print(pcos[1])
for p in range(5):
  # s = ser.read(100)       # read up to one hundred bytes
  # the structure to send the data is '\xFE <(uint_16t) VOC> <(uint_16t) VMP> <(uint_16t) IMP> <(uint_16t) ISC> \xFE'
  head = 0xFD
  Voc = 26900 #divide by 10
  Vmp = 24090 #divide by 10
  Imp = int(pcos[p]*5029) #divide by 10
  Isc = int(pcos[p]*5196) #divide by 10
  # Temperature coeff shall be applied before this
  Rs = ( Voc - Vmp ) / Imp
  a = ( Vmp * ( 1 + ( Rs*Isc ) / Voc ) + Rs*( Imp - Isc ) ) / Voc
  N = np.log( 2 - 2**a) / np.log ( Imp / Isc )
  Nl = int(N*1000) # divide by 1000
  print("Rs = %f" % Rs)
  print("a = %f" % a)
  print("N = %f" % N)
  print("Nl = %d" % Nl)
  foot = 0xFE
  #NLstr = struct.pack('!L', Nl)
  # ser.write(b'\xFE')
  ser.write(struct.pack('<B', head))
  ser.write(struct.pack('<H', Voc))
  ser.write(struct.pack('<H', Vmp))
  ser.write(struct.pack('<H', Imp))
  ser.write(struct.pack('<H', Isc))
  ser.write(struct.pack('<L', Nl))
  ser.write(struct.pack('<B', foot))
  # ser.write(0x00)
  # time.sleep(2)
  s = ser.read(1)
  print(s.hex())
  while s.hex() != 'fd':
    s = ser.read(1)
    print(s.hex())
  print("---------end of operation---------")
  head = 0xFB
  foot = 0xFC
  ser.write(struct.pack('<B', head))
  ser.write(struct.pack('<B', foot))
  s = ser.read(1)
  print(s.hex())
  if s.hex() == 'fe':
    print("---------start of operation---------")
  index = 0
  v = np.array([])
  while index < 1024:
    s = ser.read(4)
    vf = struct.unpack('<f', s)
    print(index)
    print(s.hex())
    print(vf)
    v = np.append(v, vf)
    index = index + 1  
  s = ser.read(2)
  print(s.hex())
  if s.hex() == 'fd':
    print("end of operation")
  np.savetxt("data.csv",v,delimiter=',')
  i = np.linspace(0,Isc/10,1024)
  plt.plot(v,i)


plt.show()
# for index in range(1024):
#   ser.write(struct.pack('!B', head))
#   ser.write(struct.pack('!H', index))
#   s = ser.read(2)
#   print(s.hex())
#   ser.write(struct.pack('!B', foot))
#   s = ser.read(2)
#   print(s.hex())  
#   while s.hex() != 'fd':
#       s = ser.read(2)
# ser.write(b'a')
# s = ser.read(1)
# print(s)   
ser.close()
      # check which port was really used
# Serial<id=0xa81c10, open=False>(port='COM1', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
# ser.open()
# ser.is_open
# True
# ser.close()
# ser.is_open
# False