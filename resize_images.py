import cv2
import os




folder_path = '/home/simenvg/environments/my_env/prosjektoppgave/Dataset/dark_shore_2'


for filename in os.listdir(folder_path):
	img = cv2.imread(os.path.join(folder_path,filename))
	img_resized = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
	cv2.imwrite("resized_" + filename, img_resized)
