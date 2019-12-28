import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

import glob

import random

#Root folder for data
dataPath = '/work1/s154227/data/'



# If all classes should be called fish, set this to True
oneClass = True


#Add label formats here.
#Should also include a way to process it.
VOCformat = 'VOC'


#TrainValidation split
trainSplit = 0.8


#Add the different possible class names here.
#Only the classes mentioned here will be added.
#That is, unless oneClass is True
classes = ["p virens", "p. virens", "g morhua", "h lanceolatus", "fish"]

#Sets for training on are given in path to set and file formats
#Note, there can be multiple file formats
#The last format is the type of the label




def labelData(pathToImages, fileFormatImages, pathToLabels, fileFormatLabels, labelType, VOC = True, background = True):
	all_images = []
	#Make file of images
	print(pathToImages)
	print(fileFormatImages)
	print(pathToLabels)
	print(fileFormatLabels)
	print(labelType)
	
	
	
	for fFormat in fileFormatImages:
		print("for all formats:")
		print(dataPath + pathToImages + "/images" + '/*' + fFormat)
		for f in glob.glob(dataPath + pathToImages + "/images" + '/*' + fFormat): #Add all image files
			all_images.append((f.strip(fFormat),fFormat))

	if not os.path.exists(dataPath + pathToImages + '/labels/'):
		os.makedirs(dataPath + pathToImages + '/labels/')

	list_file = open('fish.txt', 'a')
	for image_id, fFormat in all_images:
		image_id = image_id.split('/')[-1]
		if VOC:
			convert_annotation_VOC(image_id, dataPath + pathToLabels,pathToImages)
		else:
			pass
			#Already converted
		print("File: " + image_id + fFormat)
		if background:
			list_file.write(dataPath + pathToImages + "/images" + '/' + image_id + fFormat + "\n")
		else:
			if not os.stat(dataPath + pathToImages + "/labels/" + image_id + fileFormatLabels).st_size == 0:
				list_file.write(dataPath + pathToImages + "/images" + '/' + image_id + fFormat + "\n")
	list_file.close()


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation_VOC(image_id, path,pathToImages, fileFormat = '.xml'):
    in_file = open(path  + '/%s.xml'%(image_id))
    out_file = open(dataPath + pathToImages + '/labels/%s.txt'%(image_id), 'a+')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if not oneClass and (cls not in classes) or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


#Sets for training on are given in path to set and file formats
#Note, there can be multiple file formats
#The last format is the type of the label
#Add the data here:
#labelData('eyesea',['.png'],'eyesea/train_y','.xml', VOCformat)
#labelData('DTU',['.jpg'],'DTU/images','.xml', VOCformat)

try:
	os.remove("fish.txt")
except:
	pass
	
labelData('GOPR1677',['.jpg'],'GOPR1677','.txt', VOCformat, VOC = False, background = True)
labelData('GOPR0618',['.jpg'],'GOPR0618','.txt', VOCformat, VOC = False, background = True)
labelData('GOPR3043',['.jpg'],'GOPR3043','.txt', VOCformat, VOC = False, background = True)
labelData('GOPR3046',['.jpg'],'GOPR3046','.txt', VOCformat, VOC = False, background = True)
labelData('GOPR3047',['.jpg'],'GOPR3047','.txt', VOCformat, VOC = False, background = True)
labelData('DTU',['.jpg'],'DTU','.txt', VOCformat, VOC = False, background = True)





'''
labelData('eyesea',['.png'],'eyesea','.txt', VOCformat, VOC = False, background = True)

labelData('fish_01',['.png'],'fish_01','.txt', VOCformat, VOC = False, background = True)
labelData('fish_02',['.png'],'fish_02','.txt', VOCformat, VOC = False, background = True)
labelData('fish_03',['.png'],'fish_03','.txt', VOCformat, VOC = False, background = True)
labelData('fish_04',['.png'],'fish_04','.txt', VOCformat, VOC = False, background = True)
labelData('fish_05',['.png'],'fish_05','.txt', VOCformat, VOC = False, background = True)
labelData('fish_06',['.png'],'fish_06','.txt', VOCformat, VOC = False, background = True)
labelData('fish_07',['.png'],'fish_07','.txt', VOCformat, VOC = False, background = True)
labelData('fish_08',['.png'],'fish_08','.txt', VOCformat, VOC = False, background = True)
labelData('fish_09',['.png'],'fish_09','.txt', VOCformat, VOC = False, background = True)
labelData('fish_10',['.png'],'fish_10','.txt', VOCformat, VOC = False, background = True)
labelData('fish_11',['.png'],'fish_11','.txt', VOCformat, VOC = False, background = True)
labelData('fish_12',['.png'],'fish_12','.txt', VOCformat, VOC = False, background = True)
labelData('fish_13',['.png'],'fish_13','.txt', VOCformat, VOC = False, background = True)
labelData('fish_14',['.png'],'fish_14','.txt', VOCformat, VOC = False, background = True)
labelData('fish_15',['.png'],'fish_15','.txt', VOCformat, VOC = False, background = True)
labelData('fish_16',['.png'],'fish_16','.txt', VOCformat, VOC = False, background = True)
labelData('fish_17',['.png'],'fish_17','.txt', VOCformat, VOC = False, background = True)
labelData('fish_18',['.png'],'fish_18','.txt', VOCformat, VOC = False, background = True)
labelData('fish_19',['.png'],'fish_19','.txt', VOCformat, VOC = False, background = True)
labelData('fish_20',['.png'],'fish_20','.txt', VOCformat, VOC = False, background = True)
labelData('fish_21',['.png'],'fish_21','.txt', VOCformat, VOC = False, background = True)
labelData('fish_22',['.png'],'fish_22','.txt', VOCformat, VOC = False, background = True)
labelData('fish_23',['.png'],'fish_23','.txt', VOCformat, VOC = False, background = True)
'''




list_file = open('fish.txt', 'r')

all_images = list_file.readlines()

list_file.close()


random.shuffle(all_images)

train = open(dataPath + "fish_train.txt",'w')
test  = open(dataPath + "fish_valid.txt",'w')

size = len(all_images)

for i, image in enumerate(all_images):
	if i < size * trainSplit:
		train.write(image)
	else:
		test.write(image)

train.close()
test.close()
