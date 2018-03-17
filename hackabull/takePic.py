import cv2

cam = cv2.VideoCapture(0)

lowerbody_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')


def getPickForCall(imgName):
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


print 'Get the 2ft pic'
getPickForCall('lowerbody')

#print 'Get the 3ft Pic'
#getPickForCall('3ft')

#print 'Get the 4ft Pic'
#getPickForCall('4ft')



cam.release()

##destroyAllWindows()

