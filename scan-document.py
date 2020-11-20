import numpy as np
import cv2

def rescale(img,scale=0.5):
    img=cv2.resize(img,(int(img.shape[1]*scale),int(img.shape[0]*scale)),interpolation=cv2.INTER_AREA)
    return img
def empty(a):
    pass

def preProcessing(img):
    """
    preprocess the images
    """
    
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_blur=cv2.GaussianBlur(img_gray,(3,3),1)
    img_canny=cv2.Canny(img_blur,200,200)
    kernel=np.ones((5,5))
    img_dial=cv2.dilate(img_canny,kernel,iterations=2)
    img_erode=cv2.erode(img_dial,kernel,iterations=1)
    return img_erode
def getContour(img):
    biggest=np.array([])
    image,contours,hierarchy= cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>10000:
            # cv2.drawContours(img_contours,contour,-1,(0,255,0),3)
            peri=cv2.arcLength(contour,True)
            approx=cv2.approxPolyDP(contour,0.02*peri,True)
            print(len(approx))
            corner=len(approx)
            biggest=approx
        # print(biggest)
    cv2.drawContours(img_contours,biggest,-1,(0,255,0),10)
    return biggest

def getWarp(img,biggest):
    biggest=reorder(biggest)
    imgHeight,imgWeidth=800,700
    pts1=np.float32(biggest)
    pts2=np.float32([[0,0],[imgWeidth,0],[0,imgHeight],[imgWeidth,imgHeight]])
    matrix=cv2.getPerspectiveTransform(pts1,pts2)
    img_output=cv2.warpPerspective(img,matrix,(imgWeidth,imgHeight))
    img_cropped=img_output[20:img_output.shape[0]-20,20:img_output.shape[1]-20] #removing a bit of boundry
    return img_cropped

def reorder(points_init):  
    '''splitting using big y co-ordinate first and then x co-ordinate '''
    points=points_init.reshape((4,2))
    points_res=points.copy()
    sub_points2=points_res[:,1]
    newPoints=np.zeros((4,1,2),np.int32)

    lower_1,lower_position_1 =points[np.argmax(sub_points2)],np.argmax(sub_points2)
    points_res[np.argmax(sub_points2)]=-1
    sub_points2=points_res[:,1]
    lower_2,lower_position_2=points_res[np.argmax(sub_points2)],np.argmax(sub_points2)
    
    points_ress=points.copy()
    sub_points2=points_ress[:,1]

    upper_1,upper_position_1 =points[np.argmin(sub_points2)],np.argmin(sub_points2)
    points_ress[np.argmin(sub_points2)]=10000
    sub_points2=points_ress[:,1]
    upper_2,upper_position_2=points_ress[np.argmin(sub_points2)],np.argmin(sub_points2)

    if upper_1[0]<upper_2[0]:
        first_cord=upper_position_1
        second_cord=upper_position_2
    else:
        first_cord=upper_position_2
        second_cord=upper_position_1

    if lower_1[0]<lower_2[0]:
        third_cord=lower_position_1
        fourth_cord=lower_position_2
    else:
        third_cord=lower_position_2
        fourth_cord=lower_position_1
        
    # print(first_cord,second_cord,third_cord,fourth_cord)

    newPoints[0]=points[first_cord]
    newPoints[1]=points[second_cord]
    newPoints[2]=points[third_cord]
    newPoints[3]=points[fourth_cord]    
    print(newPoints)
    return newPoints

###################for image ###############
path=r'resources/'
img=cv2.imread(path+'document.jpg')
img_contours=img.copy()
img_processed=preProcessing(img)
biggest=getContour(img_processed)
img_warped=getWarp(img,biggest)
cv2.imshow('contours',img_warped)
cv2.imshow('original image',img)
cv2.imshow('img',img_contours)
cv2.waitKey(0)
############################################

######for video ################################
''' if contour not found gives error.... '''
# cap=cv2.VideoCapture(0)
# cap.set(3,300)
# cap.set(4,300)
# imgHeight,imgWeidth=1000,700
# # cap.set(10,100)  #brightness
# while True:
#     success,frame=cap.read()
#     img_contours=frame.copy()
#     cv2.resize(frame,(imgWeidth,imgHeight))
#     img_processed=preProcessing(frame)
#     biggest=getContour(img_processed)
#     img_warped=getWarp(frame,biggest)
#     cv2.imshow('video',img_warped)
#     if cv2.waitKey(1)& 0xFF==ord('q'):
#         break
################################################
