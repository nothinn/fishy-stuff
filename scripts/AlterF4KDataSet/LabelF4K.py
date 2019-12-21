import glob

import xml.etree.ElementTree as ET

from PIL import Image


i = 0
species = []
for file in glob.glob("fishPictures/fish_image/fish_23/*.png"):
    print(file)
    filename = file[32:len(file)-4]
    
    f = open("fishPictures/fish_image/fish_23/labels/" + filename +".txt", "w")

    f.write("0 0.5 0.5 0.85 0.85")

    f.close()
    


