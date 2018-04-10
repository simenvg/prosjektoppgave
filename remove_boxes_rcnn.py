import pickle
import cv2
import os
from math import sqrt, pow
from scipy.spatial import distance

folder_path = '/home/simenvg/environments/my_env/prosjektoppgave/Dataset/dark_sea'



RED = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)



def intersect_area(box_1, box_2):  # returns None if rectangles don't intersect
	dx = min(max(box_1[1][0], box_1[0][0]), box_2[1][0]) - max(min(box_1[1][0], box_1[0][0]), box_2[0][0])
	dy = min(max(box_1[1][1], box_1[0][1]), box_2[1][1]) - max(min(box_1[1][1], box_1[0][1]), box_2[0][1])
	if (dx>=0) and (dy>=0):
		return dx*dy
	else:
		return -1


def intersect_over_union(box_1, box_2):
	#print('box_1: ', box_1, '   box_2: ', box_2)
	area_box_1 = abs((box_1[1][0] - box_1[0][0]) * (box_1[1][1] - box_1[0][1]))
	area_box_2 = abs((box_2[1][0] - box_2[0][0]) * (box_2[1][1] - box_2[0][1]))
	intersection = intersect_area(box_1, box_2)
	#print('area_box_1: ', area_box_1, '   area_box_2: ', area_box_2, '  intersection: ', intersection)
	if intersection == -1:
		return -1
	else:
		return intersection / (area_box_1 + area_box_2 - intersection)


def validated_detected_objects(YOLO_boxes, GT_boxes):
	approved_boxes = []
	#print(YOLO_boxes)
	for GT_box in GT_boxes:
		#print('HEI')
		for YOLO_box in YOLO_boxes:
			#print("HALLO")
			iou = intersect_over_union(GT_box, YOLO_box)
			if iou != -1:
				pass
				#print('iou: ', iou)
			if iou >= 0.5:
				approved_boxes.append(YOLO_box)
	return approved_boxes

def get_box_center(box):
	x = abs((box[0][0] + box[1][0])/2)
	y = abs((box[0][1] + box[1][1])/2)
	return (x,y)


def euc_dist(point_1, point_2):
	return distance.euclidean(point_1, point_2)
	#return sqrt(pow(point_1[0] - point_2[0], 2) + pow(point_1[1] - opint_2[1], 2))




images_GT = pickle.load(open(os.path.join(folder_path,'ground_truth.txt'), "rb"))
images_R_CNN = pickle.load(open(os.path.join(folder_path,'dark_sea_rcnn.txt'), "rb"))

filenames = []

#print(images_R_CNN)


for keys, values in images_GT.items():
	filenames.append(keys)


images_R_CNN_iou ={}

#for key, value in images_R_CNN.items() :
    #print('filename: ', key)


#print(images_R_CNN)
for image in filenames:
	#print(images_R_CNN[image][0])
	iou_rcnn_boxes = validated_detected_objects(images_R_CNN[image][0], images_GT[image])
	images_R_CNN_iou[image] = iou_rcnn_boxes


#print(images_R_CNN)




def tangstad_remove(filenames, GT_images, rcnn_images):
	images_approved_boxes = {}

	for image in filenames:
		closest_boxes = []
		for i in range(len(GT_images[image])):
			#print(image)
			#print('HEI:   ', images_GT[image][i])
			if len(rcnn_images[image]) > 0:
				closest_box = rcnn_images[image][0]
				shortest_dist = euc_dist(get_box_center(GT_images[image][i]), get_box_center(rcnn_images[image][0]))
				for j in range(1, len(rcnn_images[image])):
					dist = euc_dist(get_box_center(GT_images[image][i]), get_box_center(rcnn_images[image][j])) 
					#print('box: ,', images_R_CNN_iou[image][j])
					#print('distance: ', dist)
					if dist < shortest_dist:	
						shortest_dist = dist
						closest_box = rcnn_images[image][j]
				closest_boxes.append(closest_box)
				#print(image)
				#print('1:   ', images_R_CNN_iou[image])
				rcnn_images[image].remove(closest_box)
		#print(closest_boxes)
				#print('2:   ', images_R_CNN_iou[image])
		images_approved_boxes[image] = closest_boxes
	return images_approved_boxes


# print('HALLO: ', rcnn_images)

# images_R_CNN_2 = tangstad_remove(filenames, images_GT, images_R_CNN_iou)

def valid_remove_boxes(filenames, rcnn_images):
	
	image_boxes = {}
	for image in filenames:
		print(image)
		#print('HEIHEI: ', rcnn_images[image])

		#print('BOXES: ', boxes)
		best_boxes = []
		if len(rcnn_images[image][0]) > 0:

			while(len(rcnn_images[image][0]) > 0):
				# best_boxes = []
				print(len(rcnn_images[image][0]))
				box = rcnn_images[image][0][0]
				score = rcnn_images[image][1][0]
				intersected_boxes = [box]
				intersected_scores = [score]
				for i in range(1, len(rcnn_images[image][0])):
					
			#		print('FADGF:  ', boxes[i])
					if intersect_over_union(box, rcnn_images[image][0][i]) > 0.5:
						intersected_boxes.append(rcnn_images[image][0][i])
						intersected_scores.append(rcnn_images[image][1][i])

				highest_score = intersected_scores[0]
				best_box = intersected_boxes[0]
				for i in range(1, len(intersected_boxes)):
					if intersected_scores[i] > highest_score:
						best_box = intersected_boxes[i]
						highest_score = intersected_scores[i]
				best_boxes.append(best_box)
				print('Best boxes:  ', best_boxes)

				for i in range(len(intersected_scores)):
					rcnn_images[image][0].remove(intersected_boxes[i])
					rcnn_images[image][1].remove(intersected_scores[i])
		image_boxes[image] = best_boxes
	return image_boxes






images_R_CNN_2 = valid_remove_boxes(filenames, images_R_CNN)

#print('gasdfgdsf  ', images_R_CNN_2)


total_true_positives = 0
total_detections = 0
undetected_objects = 0

for image in filenames:
	#print(images_GT[image])
	img = cv2.imread(os.path.join(folder_path,image))
	# approved_YOLO_boxes = validated_detected_objects(images_YOLO[image], images_GT[image])
	# for box in images_R_CNN[image]:
	# 	cv2.rectangle(img, box[0], box[1], RED, 1)
	for box in images_R_CNN_2[image]:
		cv2.rectangle(img, box[0], box[1], YELLOW, 2)
	for box in images_GT[image]:
		cv2.rectangle(img, box[0], box[1], GREEN, 1)
	cv2.imshow('image', img)
	cv2.waitKey(0)
	# total_true_positives += len(approved_YOLO_boxes)
	# total_detections += len(images_YOLO[image])
	# print('Detections: ', total_detections)
	# print('approved: ', total_true_positives)

	#undetected_objects += len()

# average_precision = total_true_positives/total_detections

# print('True positives: ', total_true_positives)
# print('False positives: ', total_detections - total_true_positives)

# print('Average precision = ', average_precision)