
import cv2
from darknetpy.detector import Detector


class Detected_object():
	def __init__(self, left, right, top, bottom, clss, prob):
		self.left = left
		self.right = right
		self.top = top
		self.bottom = bottom
		self.clss = clss
		self.prob = prob
	
	def drawBox(self, img, color):
		cv2.rectangle(img, (self.left,self.top), (self.right,self.bottom), color, 1)
		font = cv2.FONT_HERSHEY_PLAIN 
		cv2.putText(img, self.clss + ' ' + str(round(self.prob,3)), (self.left, self.top - 3),font, 0.8, color, 1)



colors = [(0,255,0), (0,0,255), (255,0,0), (255,255,0), (0,255,255), (255,0,255), (0,125,125), (125,0,125), (125,125,0)]
darknet_path = '/home/simenvg/environments/my_env/darknet'


detector = Detector(darknet_path,
                    darknet_path + '/cfg/coco.data',
                    darknet_path + '/cfg/yolo.cfg',
                    darknet_path + '/yolo.weights')



def detect(img_path):
	result = detector.detect(img_path)
	objects = []
	for elem in result:
		if elem['class'] == 'boat':
			objects.append(Detected_object(elem['left'], elem['right'], elem['top'], elem['bottom'], elem['class'], elem['prob']))
	return objects

def draw_boxes(detected_objects, img, colors):
	for i in range(len(detected_objects)):
		detected_objects[i].drawBox(img, colors[i])


impath = darknet_path + '/data/boats_clutter.png'

print('impath: ', impath)


img = cv2.imread(impath)
detected_objects = detect(impath)
draw_boxes(detected_objects, img, colors)




cv2.imshow('image', img)
cv2.waitKey(0)

