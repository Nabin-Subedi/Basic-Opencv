import cv2
import numpy as np
path=r'resources/'
faceCascade=cv2.CascadeClassifier(path+'haarcascade_frontalface_default.xml')
# bodyCascade=cv2.CascadeClassifier(path+'haarcascade_fullbody.xml')
img=cv2.imread(path+'group_1.jpg')
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces=faceCascade.detectMultiScale(img_gray,1.1,1)
print(faces.shape)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
cv2.imshow('faces',img)
cv2.waitKey(0)

