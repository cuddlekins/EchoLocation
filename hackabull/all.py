import numpy as np
import cv2
import serial 
import RPi.GPIO as GPIO

ENABLE_CAR = 0

ser = serial.Serial('/dev//ttyUSB0',9600)
#print ser.name

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

# detect if a callback for turning on the computer
# Detect if Alexa is telling the car to turn on 
GPIO.add_event_detect(21,GPIO.BOTH)
def my_callback(channel):
    global ENABLE_CAR
    if GPIO.input(21) == 1:
        ### turn on motor
	ENABLE_CAR = 1
	print 'start the motor'
    else:
        ## turn off motor
	ENABLE_CAR = 0
	print 'turn off the motor'

GPIO.add_event_detect(22,GPIO.RISING)

### Serial read interupt
def my_callback2(channel):
### Read the data
  x = ser.read()
  if x == 'L':
	### Hard turn 
	print 'Go Right'
  if x == 'R':
	### Hard turn 
	print 'Go Left'

GPIO.add_event_callback(21,callback=my_callback)
GPIO.add_event_callback(22,callback=my_callback2)

lowerbody_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

cap = cv2.VideoCapture(0)

KNOWN_WIDTH = 11.0
KNOWN_DISTANCE = 120.0
def find_marker(image):
        # convert the image to grayscale, blur it, and detect edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 35, 125)

        # find the contours in the edged image and keep the largest one;
        # we'll assume that this is our piece of paper in the image
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        c = max(cnts, key = cv2.contourArea)

        # compute the bounding box of the of the paper region and return it
        return cv2.minAreaRect(c)


def distance_to_camera(knownWidth, focalLength, perWidth):
        return (knownWidth * focalLength) / perWidth


def getTemplateMaster(imgName):
    while True:
       s,img = cam.read()
       img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       lowerbody = lowerbody_cascade.detectMultiScale(gray, 1.8, 1)
       for (x,y,w,h) in lowerbody:
          cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
          roi_color = img[y:y+h, x:x+w]
          cv2.imshow("roi_color",roi_color)
          if cv2.waitKey(25) & 0xff == ord('q'):
              cv2.imwrite(imgName+".png",roi_color)
              return roi_color
       cv2.imshow('img',img)


#getTemplateMaster('lowerbody')

image = cv2.imread("lowerbody.png")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH



img_MasterTemp = cv2.imread('lowerbody.png')
img_grayMT = cv2.cvtColor(img_MasterTemp,cv2.COLOR_BGR2GRAY)
#img_MasterTemp = cv2.resize(img_MasterTemp,(0,0),fx=2,fy=2)

while 1:
    ret, img = cap.read()
    img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lowerbody = lowerbody_cascade.detectMultiScale(gray, 1.8, 1)

#    marker = find_marker(img)
#    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
#    print inches


    for (x,y,w,h) in lowerbody:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
	marker = find_marker(img)
	inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    	print inches

	temp = roi_gray
    	w , h  = temp.shape[:2]
	res = cv2.matchTemplate(img_grayMT,temp,cv2.TM_CCOEFF_NORMED)
	thres = 0.8
	loc = np.where(res >= thres)
	for pt in zip(*loc[::-1]):
	    cv2.rectangle(img_MasterTemp,pt,(pt[0]+w,pt[1]+h),(0,255,255),2)
	    cv2.imshow('Detect',img_MasterTemp)
	    marker = find_marker(img)
    	    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
            print "found values" ,inches


	# any thing under 300 start finding it
	if inches < 300:
	    ## run the foward command
	## if value is x > w/2 turn right
	if x > w/2:
	    ## run slight right
	## if value is x < w/2 turn left
	if x < w/2:
	   ## run slight left


    cv2.imshow('img',img)
    k = cv2.waitKey(5) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
