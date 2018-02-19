import pickle
import cv2
import os



folder_path = '/home/simenvg/environments/my_env/prosjektoppgave/boats'


RED = (0,0,255)
GREEN = (0,255,0)



images_GT = pickle.load(open(os.path.join(folder_path,'ground_truth.txt'), "rb"))
images_YOLO = pickle.load(open(os.path.join(folder_path,'YOLO.txt'), "rb"))

filenames = []

for keys, values in images_GT.items():
	filenames.append(keys)


for image in filenames:
	print(images_GT[image])
	img = cv2.imread(os.path.join(folder_path,image))
	for box in images_YOLO[image]:
		cv2.rectangle(img, box[0], box[1], RED, 1)
	for box in images_GT[image]:
		cv2.rectangle(img, box[0], box[1], GREEN, 1)
	cv2.imshow('image', img)
	cv2.waitKey(0)