import glob

import xml.etree.ElementTree as ET

from PIL import Image


i = 0
species = []
for file in glob.glob("Simon/finished_labels_and_img/*.xml"):
    print(file)
    tree = ET.parse(file)


    image_orig = Image.open("Simon/finished_labels_and_img/" + tree.getroot().find("filename").text)


    objects = tree.getroot().findall("object")

    for obj in objects:
        name = obj.find("name").text
        bndbox = obj.find("bndbox")

        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        
        cropped = image_orig.crop((xmin, ymin, xmax, ymax))

        cropped.save("extracted/{}.jpg".format(i))

        species.append(str(i) + "; " + name)

        i += 1


with open('all_fish.txt', 'w') as f:
    for item in species:
        f.write("%s\n" % item)
