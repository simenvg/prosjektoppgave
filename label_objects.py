import cv2
import os
import numpy as np
import copy



folder_path = ""
start_point = (-1,-1)
end_point = (-1,-1)

def draw_rectangle(event, x, y, flags, params):
    global start_point, end_point
    if event == cv2.EVENT_LBUTTONDOWN:
         print('Start Mouse Position: '+str(x)+', '+str(y))
         start_point = (x, y)
    if event == cv2.EVENT_LBUTTONUP:
        print('End Mouse Position: '+str(x)+', '+str(y))
        end_point = (x, y)
        cv2.rectangle(img, start_point, end_point, (255,0,0), 1)


# for filename in os.listdir(folder):
#     img = cv2.imread(os.path.join(folder,filename))
#     cv2.imshow('img', img)
#     if img is not None:
#         images.append(img)


img = np.zeros((512,512,3), np.uint8)
img_true = copy.copy(img)
img_backup = copy.copy(img)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_rectangle)


boxes = []

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) #& 0xFF
    if k == 27:
        break
    elif k== -1:
        continue
    elif k == 8: #backspace
        img = copy.copy(img_true)
    elif k == 13: # return
        img_true = copy.copy(img)
    elif k == 80: # home
        img = copy.copy(img_backup)
        img_true = copy.copy(img)
    else:
        print(k)


cv2.destroyAllWindows()

