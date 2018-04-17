import os
import pickle


folderpath = '/home/simenvg/environments/my_env/prosjektoppgave/score_box/light_sea_rcnn'

images = {}

scores_path = folderpath + '/scores'
boxes_path =  folderpath + '/boxes'

# print(scores_path)

scores = sorted(os.listdir(folderpath + '/scores'))
boxes  = sorted(os.listdir(folderpath + '/boxes'))


# for i in range(len(scores)):
#     print(scores[i])
#     print(boxes[i])




images ={}

for i in range(len(scores)):    # Looper gjennom bilder
    print('########################')
    approved_boxes = []
    box_scores = []

    with open(os.path.join(scores_path, scores[i])) as f:
        #print('hei')
        image_scores = f.readlines()
    image_scores = [x.strip() for x in image_scores] 
    
    with open(os.path.join(boxes_path, boxes[i])) as fi:
        image_boxes = fi.readlines()
    image_boxes = [x.strip() for x in image_boxes]

    for j in range(len(image_scores)):
        if float(image_scores[j]) >= 0.25:
            #print(image_scores[j])
            #print('GDFSHFH')
            approved_boxes.append(image_boxes[j])
            box_scores.append(image_scores[j])
    #print(approved_boxes)

    filename = scores[i][:-4]
    filename = filename.replace("_scores", "")
    filename = filename + ".jpg"
    print(filename)
    # [(left, top), (right, bottom)]

    objects = []

    for elem in image_boxes:
        elem = elem.replace("'", "")
        lst = elem.split(",")
        
        objects.append([(int(float(lst[0])), int(float(lst[1]))), (int(float(lst[2])), int(float(lst[3])))])
        #print(objects)

    images[filename] = (objects, image_scores)
    print(filename)
    #print(images)

#print(images)
pickle.dump(images, open(os.path.join(folderpath,'light_sea_rcnn.txt'), "wb"))
