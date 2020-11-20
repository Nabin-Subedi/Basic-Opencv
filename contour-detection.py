import cv2
import numpy as np

def rescale(img,scale=0.5):
    img=cv2.resize(img,(int(img.shape[1]*scale),int(img.shape[0]*scale)),interpolation=cv2.INTER_AREA)
    return img
def getObject(corner):
    objects=['none','none','none','triangle','rect/rmbus','pentagon','hexagon','circle','octagon/cir']
    return objects[corner]
def getContour(img):
    image,contours,hierarchy= cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>500:
            cv2.drawContours(img_contours,contour,-1,(0,255,0),3)
            peri=cv2.arcLength(contour,True)
            approx=cv2.approxPolyDP(contour,0.02*peri,True)
            print(len(approx))
            corner=len(approx)
            text=getObject(corner)
            print(text)
            x,y,w,h=cv2.boundingRect(approx)
            cv2.rectangle(img_contours,(x,y),(x+w,y+h),(0,0,255),3)
            cv2.putText(img_contours,text,(x+(w//2)-40,y+(h//2)-40),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        #print(area)

path=r'resources/'
img=cv2.imread(path+'shapes_1.jpg')
img=rescale(img,scale=0.3)
img_contours=img.copy()

img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_blur=cv2.GaussianBlur(img_gray,(5,5),1)
img_canny=cv2.Canny(img_blur,70,70)
getContour(img_canny)
cv2.imshow('Shapes',img )
#cv2.imshow('Shapes gray',img_gray)
cv2.imshow('Shapes blur',img_blur)
cv2.imshow('Shapes canny',img_canny)
cv2.imshow('Shapes cont',img_contours)

cv2.waitKey(0)