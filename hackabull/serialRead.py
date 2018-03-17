import serial 

ser = serial.Serial('/dev//ttyUSB0',9600)
print ser.name
while 1:
  x = ser.read()
  if x == 'L':
	print 'Go Right'
  if x == 'R':
	print 'Go Left'
  #print x
