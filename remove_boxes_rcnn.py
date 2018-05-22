import pickle
import cv2
import os
from math import sqrt, pow
from scipy.spatial import distance
import copy
from matplotlib import pyplot as plt



folder = 'resized_dark_shore'

folder_path = '/home/simenvg/environments/my_env/prosjektoppgave/Dataset/' + folder


BLUE = (255,0,0)
RED = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)



def intersect_area(box_1, box_2):  # returns None if rectangles don't intersect
	dx = min(max(box_1[1][0], box_1[0][0]), box_2[1][0]) - max(min(box_1[1][0], box_1[0][0]), box_2[0][0])
	dy = min(max(box_1[1][1], box_1[0][1]), box_2[1][1]) - max(min(box_1[1][1], box_1[0][1]), box_2[0][1])
	#print('dx: ', dx, '    dy: ', dy)
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


def validated_detected_objects(detected_boxes, GT_boxes):
	approved_boxes = []

	temp_detected_boxes = copy.copy(detected_boxes)


	#print('TEMP: ', temp_detected_boxes)
	#print('GT_boxes:  ', GT_boxes)
	for GT_box in GT_boxes:
	#	print('HEISANN')

		if len(temp_detected_boxes) > 0:
			found_box = False
			best_iou = intersect_over_union(GT_box, temp_detected_boxes[0])
			if best_iou >= 0.5:
				found_box = True
	#		print('best_iou: ', best_iou)
			best_box = temp_detected_boxes[0]
			
			for i in range(1, len(temp_detected_boxes)):
				#print("HALLO")
				iou = intersect_over_union(GT_box, temp_detected_boxes[i])
	#			print('iou: ', iou)
				#if iou != -1:
				#	pass
					#print('iou: ', iou)
				if iou >= 0.5 and iou > best_iou:
					#print(iou)
					found_box = True
					best_box = temp_detected_boxes[i]
					best_iou = iou
			if found_box:
				approved_boxes.append(best_box)
				temp_detected_boxes.remove(best_box)
	return approved_boxes

def get_box_center(box):
	x = abs((box[0][0] + box[1][0])/2)
	y = abs((box[0][1] + box[1][1])/2)
	return (x,y)


def euc_dist(point_1, point_2):
	return distance.euclidean(point_1, point_2)
	#return sqrt(pow(point_1[0] - point_2[0], 2) + pow(point_1[1] - opint_2[1], 2))




images_GT = pickle.load(open(os.path.join(folder_path,'ground_truth.txt'), "rb"))
images_R_CNN = pickle.load(open(os.path.join(folder_path,(folder + '_rcnn.txt')), "rb"))

images_R_CNN_2 = copy.deepcopy(images_R_CNN)

filenames = []

#print(images_R_CNN)

num_GT_boxes = 0

for keys, values in images_GT.items():
	filenames.append(keys)
	num_GT_boxes += len(values)

print('num: ', num_GT_boxes)


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
		best_boxes = []
		scores = []
		if len(rcnn_images[image][0]) > 0:

			while(len(rcnn_images[image][0]) > 0):
				# best_boxes = []
				#print(len(rcnn_images[image][0]))
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
				scores.append(float(highest_score))
				#print('Best boxes:  ', best_boxes)

				for i in range(len(intersected_scores)):
					rcnn_images[image][0].remove(intersected_boxes[i])
					rcnn_images[image][1].remove(intersected_scores[i])
		#print('scores: ', len(scores), '  boxes: ', len(best_boxes))
		image_boxes[image] = (best_boxes, scores)
	return image_boxes




images_YOLO = pickle.load(open(os.path.join(folder_path,'YOLO.txt'), "rb"))
images_R_CNN_tangstad = tangstad_remove(filenames, images_GT, images_R_CNN_iou)


images_R_CNN_conf_over_25 = {}
lol2 = copy.deepcopy(images_R_CNN)


for key, value in images_R_CNN.items():
	boxes = []
	scores = []
	for i in range(len(value[0])):
		if float(value[1][i]) >= 0.5:
			boxes.append(value[0][i])
			scores.append(value[1][i])
	images_R_CNN_conf_over_25[key] = (boxes, scores)

lol = copy.deepcopy(images_R_CNN_conf_over_25)


images_R_CNN_valid_over_25 = valid_remove_boxes(filenames, lol)
images_R_CNN_valid = valid_remove_boxes(filenames, lol2)

#print('length: ', len(images_R_CNN_valid[folder + '_1.jpg'][0]))

#print(images_R_CNN_valid)
#print('gasdfgdsf  ', images_R_CNN_2)

images_YOLO_conf_over_25 = {}

for key, value in images_YOLO.items():
	boxes = []
	scores = []
	for i in range(len(value[0])):
		if value[1][i] >= 0.25:
			boxes.append(value[0][i])
			scores.append(value[1][i])
	images_YOLO_conf_over_25[key] = (boxes, scores)







def get_precision(filenames, GT_boxes, detected_boxes):
	sum_detected_objects = 0
	sum_true_positives = 0
	for image in filenames:
		#print(image)
		sum_detected_objects += len(detected_boxes[image][0])
		sum_true_positives += len(validated_detected_objects(detected_boxes[image][0], GT_boxes[image]))
		#print('Num detected objects: ', sum_detected_objects)
		#print('Num true positives: ', sum_true_positives)
	if sum_detected_objects == 0:
		return -1
	return sum_true_positives / sum_detected_objects

def get_recall(filenames, GT_boxes, detected_boxes):
	sum_GT_boxes = 0
	sum_true_positives = 0
	for image in filenames:
		sum_GT_boxes += len(GT_boxes[image])
		sum_true_positives += len(validated_detected_objects(detected_boxes[image][0], GT_boxes[image]))
		#print('GT: ', sum_GT_boxes, '   TP: ', sum_true_positives)
	return sum_true_positives / sum_GT_boxes



def boxes_based_on_score(filenames, detected_boxes, conf_level):
	images = {}
	for image in filenames:
		boxes = []
		scores = []
		for i in range(len(detected_boxes[image][0])):
			if float(detected_boxes[image][1][i]) > conf_level:
				boxes.append(detected_boxes[image][0][i])
				scores.append(float(detected_boxes[image][1][i]))
		images[image] = (boxes, scores)
	return images




def plot_precision_recall(yolo_prec_recall, rcnn_prec_recall, rcnn_prec_recall_removed_boxes, title):
	# print('Availible variables to plot: {}'.format(history.history.keys()))
	fig_1, ax_1 = plt.subplots()
	#fig_2, ax_2 = plt.subplots()
	for i in range(len(yolo_prec_recall[0])):
		if yolo_prec_recall[0][i] != -1:
			ax_1.plot(yolo_prec_recall[1][i], yolo_prec_recall[0][i], 'o', color='red', label='YOLO')#, AP: ' + str(round(get_average_precision(yolo_prec_recall),2)))
		if rcnn_prec_recall[0][i] != -1:
			ax_1.plot(rcnn_prec_recall[1][i], rcnn_prec_recall[0][i], 'X', color='blue', label='Faster R-CNN')#, AP: ' + str(round(get_average_precision(rcnn_prec_recall), 2)))
		if rcnn_prec_recall_removed_boxes[0][i] != -1:
			print("HEEEEI   :", rcnn_prec_recall_removed_boxes[1][i])
			ax_1.plot(rcnn_prec_recall_removed_boxes[1][i], rcnn_prec_recall_removed_boxes[0][i], 'D', color='green', label='Faster R-CNN removed boxes')#, AP: ' + str(round(get_average_precision(rcnn_prec_recall_removed_boxes), 2)))
	ax_1.set_title(title)
	#txt = "YOLO AP: " + str(get_average_precision(yolo_prec_recall)) + "   Faster R-CNN AP: " + str(get_average_precision(rcnn_prec_recall)) + "  Faster R-CNN removed boxes AP: " + str(get_average_precision(rcnn_prec_recall_removed_boxes))
	#plt.figtext(2,6, txt)
	plt.legend()
	plt.xlabel('Recall')
	plt.ylabel('Precision')
	plt.show()



thresholds = [0.999, 0.99]

a = 0.95
while a >= 0.01:
	thresholds.append(a)
	a -= 0.01

thresholds.extend([0.001, 0.000001, 0.0000000001])

# thresholds = [0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# print(thresholds)


def generate_recall_and_precisions(filenames, GT_boxes, detected_boxes, thresholds, remove_boxes=False):
	recalls = []
	precisions = []
	for elem in thresholds:
		if remove_boxes == False:
			recalls.append(get_recall(filenames, GT_boxes, boxes_based_on_score(filenames, detected_boxes, elem)))
			precisions.append(get_precision(filenames, GT_boxes, boxes_based_on_score(filenames, detected_boxes, elem)))
		else:
			boxes_over_score = boxes_based_on_score(filenames, detected_boxes, elem)
			valid_boxes_over_score = valid_remove_boxes(filenames, boxes_over_score)
			recalls.append(get_recall(filenames, GT_boxes, valid_boxes_over_score))
			precisions.append(get_precision(filenames, GT_boxes, valid_boxes_over_score))
	return (precisions, recalls)


def get_average_precision(prec_recall):
	precisions = prec_recall[0]
	sum_precisions = 0
	num_prec = 0
	for elem in precisions:
		#print(elem)
		if elem != -1:
			sum_precisions += elem
			num_prec += 1
	return sum_precisions/num_prec


#yolo_prec_recall = generate_recall_and_precisions(filenames, images_GT, images_YOLO, thresholds)
#print("###")
#rcnn_prec_recall = generate_recall_and_precisions(filenames, images_GT, images_R_CNN_2, thresholds)
#print('#####')
#rcnn_prec_recall_removed_boxes = generate_recall_and_precisions(filenames, images_GT, images_R_CNN_2, thresholds, remove_boxes=True)
#print(images_R_CNN_2[folder + '_1.jpg'])
# print(images_R_CNN_valid)

# fig, ax = plt.subplots()

# ax.plot(yolo_recall, yolo_prec, 'o', color='C0')
# plt.show()

#print('PREC_RECALL:  ', rcnn_prec_recall_removed_boxes)
#print('YOLO AP: ', get_average_precision(yolo_prec_recall))
#print('Faster R-CNN AP: ', get_average_precision(rcnn_prec_recall))
#print('Faster R-CNN removed boxes AP: ', get_average_precision(rcnn_prec_recall_removed_boxes))

#plot_precision_recall(yolo_prec_recall, rcnn_prec_recall, rcnn_prec_recall_removed_boxes, folder)



def draw_boxes(image_name, GT_boxes, detected_boxes):
	validated_boxes = validated_detected_objects(detected_boxes, GT_boxes)
	img = cv2.imread(os.path.join(folder_path,image_name))
	validated_boxes_n = 0
	gt_boxes_n = 0
	for box in detected_boxes:
		cv2.rectangle(img, box[0], box[1], RED, 1)
	for box in validated_boxes:
		cv2.rectangle(img, box[0], box[1], BLUE, 2)
		validated_boxes_n += 1
	for box in GT_boxes:
		cv2.rectangle(img, box[0], box[1], GREEN, 1)
		gt_boxes_n += 1
	cv2.imshow(image_name, img)
	cv2.waitKey(0)
	return (validated_boxes_n, gt_boxes_n)


# v = 0
# b = 0
# for image in filenames:
# 	(val_b, gt_b) = draw_boxes(image, images_GT[image], images_R_CNN_valid_over_25[image][0])
# 	v += val_b
# 	b += gt_b

# print(v, '    ', b, '    ', v/b)
# # image = 'light_shore_24.jpg'

# draw_boxes(image, images_GT[image], images_YOLO_conf_over_25[image][0])
# draw_boxes(image, images_GT[image], images_R_CNN_conf_over_25[image][0])
# draw_boxes(image, images_GT[image], images_R_CNN_valid_over_25[image][0])