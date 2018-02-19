import pickle
import cv2
import os

folder_path = '/home/simenvg/environments/my_env/prosjektoppgave/boats'



RED = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)


box_1 = [(0, 0), (5, 5)]
box_2 = [(1, 1), (5, 7)]
# intersection here is (3, 3, 4, 3.5), or an area of 1*.5=.5

def intersect_area(box_1, box_2):  # returns None if rectangles don't intersect
	dx = min(box_1[1][0], box_2[1][0]) - max(box_1[0][0], box_2[0][0])
	dy = min(box_1[1][1], box_2[1][1]) - max(box_1[0][1], box_2[0][1])
	if (dx>=0) and (dy>=0):
		return dx*dy
	else:
		return -1


def intersect_over_union(box_1, box_2):
	area_box_1 = (box_1[1][0] - box_1[0][0]) * (box_1[1][1] - box_1[0][1])
	area_box_2 = (box_2[1][0] - box_2[0][0]) * (box_2[1][1] - box_2[0][1])
	intersection = intersect_area(box_1, box_2)
	if intersection == -1:
		return -1
	else:
		return intersection / (area_box_1 + area_box_2 - intersection)


def validated_detected_objects(YOLO_boxes, GT_boxes):
	approved_boxes = []
	for GT_box in GT_boxes:
		highest_iou = 0 
		for YOLO_box in YOLO_boxes:
			iou = intersect_over_union(GT_box, YOLO_box)
			print('iou: ', iou)
			if iou >= 0.5 and iou > highest_iou:
				approved_boxes.append(YOLO_box)
				print('HEFIAE')
	return approved_boxes





images_GT = pickle.load(open(os.path.join(folder_path,'ground_truth.txt'), "rb"))
images_YOLO = pickle.load(open(os.path.join(folder_path,'YOLO.txt'), "rb"))

filenames = []

for keys, values in images_GT.items():
	filenames.append(keys)




for image in filenames:
	print(images_GT[image])
	img = cv2.imread(os.path.join(folder_path,image))
	approved_YOLO_boxes = validated_detected_objects(images_YOLO[image], images_GT[image])
	for box in images_YOLO[image]:
		cv2.rectangle(img, box[0], box[1], RED, 1)
	for box in approved_YOLO_boxes:
		cv2.rectangle(img, box[0], box[1], YELLOW, 2)
	for box in images_GT[image]:
		cv2.rectangle(img, box[0], box[1], GREEN, 1)
	cv2.imshow('image', img)
	cv2.waitKey(0)