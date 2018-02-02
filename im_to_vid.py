import cv2
import numpy as np
import os


path = '/home/simenvg/environments/my_env/prosjektoppgave/images'

height = 320
width = 1920

img=[]
list_im = []

output = 'output.mp4'


for i in range(1,1025):
	list_im.append(os.path.join(path, 'image_'+str(i*6)+'.png'))


fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))



for image in list_im:
    image_path = os.path.join(path, image)
    frame = cv2.imread(image_path)

    out.write(frame) # Write out frame to video

    cv2.imshow('video',frame)
    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break



# for j in range(len(img)):
#     video.write(img[j])

cv2.destroyAllWindows()
out.release()

print("The output video is {}".format(output))