import cv2
import numpy as np

def rescale(img,scale=0.5):
    img=cv2.resize(img,(int(img.shape[1]*scale),int(img.shape[0]*scale)),interpolation=cv2.INTER_AREA)
    return img

def empty(a):
    pass

path=r'resources/'

cv2.namedWindow('tracker')
cv2.resizeWindow('tracker',640,250)
cv2.createTrackbar('hue min','tracker',21,179,empty)
cv2.createTrackbar('hue max','tracker',72,179,empty)
cv2.createTrackbar('saturation min','tracker',90,255,empty)
cv2.createTrackbar('saturation max','tracker',255,255,empty)
cv2.createTrackbar('val min','tracker',34,255,empty)
cv2.createTrackbar('val max','tracker',255,255,empty)


while True:
    img=cv2.imread(path+'lambo.jpg')
    img=rescale(img,scale=0.2)
    img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min=cv2.getTrackbarPos('hue min','tracker')
    h_max=cv2.getTrackbarPos('hue max','tracker')
    s_min=cv2.getTrackbarPos('saturation min','tracker')
    s_max=cv2.getTrackbarPos('saturation max','tracker')
    v_min=cv2.getTrackbarPos('val min','tracker')
    v_max=cv2.getTrackbarPos('val max','tracker')
    #print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv2.inRange(img_hsv,lower,upper)
    img_output=cv2.bitwise_and(img,img,mask=mask)
    #cv2.imshow('lambo',img)
    cv2.imshow('lambo_HSV',img_hsv)
    cv2.imshow('lambo_HSV_mask',mask)
    cv2.imshow('output',img_output)

    if cv2.waitKey(1)& 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
