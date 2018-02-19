import pickle
import cv2
import os

folder_path = '/home/simenvg/environments/my_env/prosjektoppgave/boats'







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
	return intersection / (area_box_1 + area_box_2 - intersection)




