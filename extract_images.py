import glob

import xml.etree.ElementTree as ET

from PIL import Image


i = 0
species = []
for file in glob.glob("../../Simon/finished_labels_and_img/*.xml"):
    print(file)
    tree = ET.parse(file)


    image_orig = Image.open("../../Simon/finished_labels_and_img/" + tree.getroot().find("filename").text)
    width, height = image_orig.size
    
    objects = tree.getroot().findall("object")

    no_obj = True
    
    for obj in objects:
        no_obj = False
        name = obj.find("name").text
        bndbox = obj.find("bndbox")

        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)

        xdist = xmax - xmin
        ydist = ymax - ymin

        diff = abs(xdist - ydist)

        if xdist >= ydist:
            ymin -= diff//2
            ymax += diff//2
            if ymin < 0:
                ymin = 0
                ymax = xdist
            elif ymax > height:
                ymax = height
                ymin = height - xdist
        else:
            xmin -= diff//2
            xmax += diff//2
            if xmin < 0:
                xmin = 0
                xmax = ydist
            elif xmax > width:
                xmax = width
                xmin = width-ydist

        
        cropped = image_orig.crop((xmin, ymin, xmax, ymax))

        cropped.save("extracted/{}.jpg".format(i))

        species.append(str(i) + "; " + name)

        i += 1
    
    if no_obj:
        background = image_orig.crop((0, 0, min(width, height), min(width, height)))
        background.save("extracted/{}.jpg".format(i))

        species.append(str(i) + "; background")
        i += 1


with open('all_fish.txt', 'w') as f:
    for item in species:
        f.write("%s\n" % item)
