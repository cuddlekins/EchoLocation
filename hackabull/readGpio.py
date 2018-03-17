import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

# detect if a raise 
GPIO.add_event_detect(21,GPIO.BOTH)
def my_callback(channel):
    if GPIO.input(21) == 1:
        ### turn on motor
	print 'start the motor'
    else:
        ### turn off motor
	print 'turn off the motor'

GPIO.add_event_callback(21,callback=my_callback)

while 1:
 x=5
