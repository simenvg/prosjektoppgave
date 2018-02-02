import numpy as np
import cv2
import pywt



wl = 'db5' # Daubechies

# data = np.ones((4,4), dtype=np.float64)
# coeffs = pywt.dwt2(data, wl)
# print(coeffs[0]) # LL subband
# print('HEIEHIEHI')

def w2d(img, mode='haar', level=1):
    #img = cv2.imread(img)
    #Datatype conversions
    #convert to grayscale
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    #convert to float
    img =  np.float32(img)   
    img /= 255;
    # compute coefficients 
    coeffs=pywt.wavedec2(img, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)
    #Display result
    # cv2.imshow('image',imArray_H)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return imArray_H



cap = cv2.VideoCapture('hurtig_3min.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = 20)


while(1):
    ret, frame = cap.read()
    
    frame_lp = w2d(frame, wl,6)
    (thresh, lp_bw) = cv2.threshold(frame_lp, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    (thresh, fr_bw) = cv2.threshold(frame, 180, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(lp_bw)
    # cv2.subtract(fr_bw,lp_bw)
    cv2.imshow('frame',fgmask)
    cv2.imshow('lp',fgmask2)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()