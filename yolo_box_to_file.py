import cv2
from darknetpy.detector import Detector
import os
import pickle
import sys

print(sys.path)

darknet_path = '/home/simenvg/environments/my_env/darknet'
###'/home/simenvg/environments/my_env/prosjektoppgave/Dataset/resized_dark_shore', 
folder_paths = ['/home/simenvg/environments/my_env/prosjektoppgave/Dataset/resized_dark_shore', '/home/simenvg/environments/my_env/prosjektoppgave/Dataset/light_shore', '/home/simenvg/environments/my_env/prosjektoppgave/Dataset/light_sea', '/home/simenvg/environments/my_env/prosjektoppgave/Dataset/dark_sea' ]

detector = Detector(darknet_path,
                    darknet_path + '/cfg/coco.data',
                    darknet_path + '/cfg/yolo.cfg',
                    darknet_path + '/yolo.weights')


images = {}


def detect(img_path):
	result = detector.detect(img_path, 0.0000000001)
	objects = []
	scores = []
	for elem in result:
		print(elem)
		if elem['class'] == 'boat':# and float(elem['prob']) > 0.24:
			objects.append([(elem['left'], elem['top']),(elem['right'], elem['bottom'])])
			scores.append(float(elem['prob']))
	return (objects, scores)


for folder_path in folder_paths:
	for filename in os.listdir(folder_path):
		if filename[len(filename)-3:] == 'txt':
			continue
		boxes = detect(os.path.join(folder_path,filename))
		print(boxes)
		images[filename] = boxes


	pickle.dump(images, open(os.path.join(folder_path,'YOLO.txt'), "wb"))
	images = {}
