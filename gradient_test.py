import cv2
import numpy as np
from matplotlib import pyplot as plt
darknet_path = '/home/simenvg/environments/my_env/darknet'
impath = darknet_path + '/data/boat.png'



im = cv2.imread(impath)
im = np.float32(im) / 255.0
 
# Calculate gradient 
gx = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=1)
gy = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=1)

# Python Calculate gradient magnitude and direction ( in degrees ) 
mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)


#Harris corners on gradient image, coastline suppressed.
cv2.imshow('image', mag)
gray = cv2.cvtColor(mag,cv2.COLOR_BGR2GRAY)
 
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,3,3,0.04)
 
 #result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
 
# Threshold for an optimal value, it may vary depending on the image.
mag[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',mag)
cv2.waitKey(0)




