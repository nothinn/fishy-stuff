from PIL import Image
import numpy as np
import glob
import os

def normalize(arr):
    """
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    arr = arr.astype('float')
    # Do not touch the alpha channel
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (255.0/(maxval-minval))
    return arr

for filename in os.listdir('../../../Jacob/fishy-stuff/scripts/'): #videos/images/
    if filename.endswith(".jpg"):
        img = Image.open(filename)
        arr = np.array(img)
        new_img = Image.fromarray(normalize(arr).astype('uint8'),'RGB')
        image_path_and_name = os.path.split(filename) 
        image_name_and_ext = os.path.splitext(image_path_and_name[1]) 
        name = image_name_and_ext[0] + '.jpg'
        new_img.save('../../../Jacob/fishy-stuff/scripts/img/' + name) #videos/norm_images/
        print("All good")