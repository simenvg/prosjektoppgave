import cv2
import numpy as np
from matplotlib import pyplot as plt
darknet_path = '/home/simenvg/environments/my_env/darknet'
impath = darknet_path + '/data/boat.png'



def sobel(img):
	img = np.float32(img) / 255.0
	# Calculate gradient 
	gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
	gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)
	# Python Calculate gradient magnitude and direction ( in degrees ) 
	mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
	return mag

def blur(img, dim):
	return cv2.GaussianBlur(img, (dim,dim), 0)

def harris(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	 
	gray = np.float32(gray)
	dst = cv2.cornerHarris(gray,3,3,0.04)
	 
	# result is dilated for marking the corners, not important
	dst = cv2.dilate(dst,None)
	# Threshold for an optimal value, it may vary depending on the image.
	img[dst>0.01*dst.max()]=[0,0,255]


img = cv2.imread(impath)

im_sobel = sobel(img)
cv2.imshow('sobel', im_sobel)
im_blur = blur(im_sobel, 3)
im_blur = blur(im_blur, 5)
cv2.imshow('blur', im_blur)
im_harr = im_sobel
harris(im_harr)
im_blur_harr = im_blur
harris(im_blur_harr)






cv2.imshow('harris', im_harr)
	
cv2.imshow('harris blur', im_blur_harr)
cv2.waitKey(0)




