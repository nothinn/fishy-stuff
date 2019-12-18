from flask import Flask, request, url_for,send_file
from flask_cors import CORS
import os, random
import shutil 
import json
from pathlib import Path
import cv2
import base64

app = Flask(__name__)
CORS(app)

a = []
picturesWithFish = []
unknownS = []
backgroundS = []
correctLabelingS = []
#anthon = True
simon = True
# picturePath = "X:/videos/images"
# pathasa = "X:/Frederik/fishy-stuff/scripts/resultSimonFishDetected.json"
# path = "X:/Frederik/fishy-stuff/scripts/pictures"
# backgroundSpath = "X:/Frederik/fishy-stuff/scripts/pictures/backgroundS.json"
# correctLabelingSpath = "X:/Frederik/fishy-stuff/scripts/pictures/correctLabelingS.json"  
# unknownSpath = "X:/Frederik/fishy-stuff/scripts/unknownS.json"
picturePath = "/work1/s154227/videos/norm_images"
pathasa = ""
path = "/work1/s154227/Frederik/fishy-stuff/scripts/pictures"
backgroundSpath = ""
correctLabelingSpath = ""  
unknownSpath = ""
un = ""
correct = ""
back = ""
resultJson = ""

if simon:
    resultJson = "resultNetworksJson/resultSimonFishDetected_v3.json"
    pathasa = "/work1/s154227/Frederik/fishy-stuff/scripts/resultNetworksJson/resultSimonFishDetected_v3.json"
    backgroundSpath = "/work1/s154227/Frederik/fishy-stuff/scripts/pictures/backgroundS.json"
    correctLabelingSpath = "/work1/s154227/Frederik/fishy-stuff/scripts/pictures/correctLabelingS.json"  
    unknownSpath = "/work1/s154227/Frederik/fishy-stuff/scripts/pictures/unknownS.json"
    un = "unknownS.json"
    correct = "correctLabelingS.json"
    back = "backgroundS.json"
else:
    resultJson = "resultNetworksJson/resultAnthonFishDetected_v2.json"
    pathasa = "/work1/s154227/Frederik/fishy-stuff/scripts/resultNetworksJson/resultAnthonFishDetected_v2.json"
    backgroundSpath = "/work1/s154227/Frederik/fishy-stuff/scripts/pictures/backgroundA.json"
    correctLabelingSpath = "/work1/s154227/Frederik/fishy-stuff/scripts/pictures/correctLabelingA.json"  
    unknownSpath = "/work1/s154227/Frederik/fishy-stuff/scripts/pictures/unknownA.json"
    un = "unknownA.json"
    correct = "correctLabelingA.json"
    back = "backgroundA.json"


width = 1280
height = 720

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(x,y,w,h, img, confidence):
    xmin, ymin, xmax, ymax = convertBack(
        float(x), float(y), float(w), float(h))
    pt1 = (xmin, ymin)
    pt2 = (xmax, ymax)
    print(pt1,pt2)
    cv2.rectangle(img, pt1, pt2, (0, 0, 255), 1)
    cv2.putText(img,
                "fish c: " + str(confidence),
                (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                [0, 255, 0], 2)
    return img

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        ob = request.json["Pictures"]

        for i in range(len(ob)):
            indexPic = next(pic for pic in range(len(picturesWithFish)) if picturesWithFish[pic]["filename"] == ob[i]["filename"])
            if ob[i]["background"] and ob[i]["fishCorrectOnpicture"]:
                print("User did something wring do not delte yet")
            elif ob[i]["background"]:
                whole = picturesWithFish.pop(indexPic)
                backgroundS.append(whole)
            elif ob[i]["fishCorrectOnpicture"]:
                whole = picturesWithFish.pop(indexPic)
                correctLabelingS.append(whole)
            else:
                whole = picturesWithFish.pop(indexPic)
                unknownS.append(whole)
        
        with open('pictures/' + un, 'w') as json_file:
            json.dump(unknownS, json_file)

        with open('pictures/' + back, 'w') as json_file:
            json.dump(backgroundS, json_file)

        with open('pictures/' + correct, 'w') as json_file:
            json.dump(correctLabelingS, json_file)
        
        with open(resultJson, 'w') as json_file:
            json.dump(picturesWithFish, json_file)

        # falsePath = "X:/Frederik/fishy-stuff/scripts/pictures/VerifiedFalse"
        # truePath = "X:/Frederik/fishy-stuff/scripts/pictures/VerifiedTrue"  
        # path = "X:/Frederik/fishy-stuff/scripts/pictures/Unverified"    
        # files = sorted(os.listdir(path))
        # ob = request.json
        # print(len(ob["Pictures"]))
        # for i in range(len(ob["Pictures"])):
        #     if ob["Pictures"][i]["value"]:
        #         shutil.move(path + "/" + files[int(ob["Pictures"][i]["count"])], truePath + "/" + files[int(ob["Pictures"][i]["count"])])
        #     else:
        #         shutil.move(path + "/" + files[int(ob["Pictures"][i]["count"])], falsePath + "/" + files[int(ob["Pictures"][i]["count"])])
        return "Happy days"
    
    return "Error"
    # elif request.method == 'GET':

@app.route('/', methods=['GET'])
def getPictures():
    if request.method == 'GET':
        picts = []
        for i in range(24):
            picture = picturesWithFish[i]
            if not os.path.exists(picturePath + "/" + picture["filename"].split("/")[-1]):
                continue
            image = cv2.imread(picturePath + "/" + picture["filename"].split("/")[-1])
            
            for i in range(len(picturesWithFish[i]["objects"])):
                x = picture["objects"][i]["relative_coordinates"]["center_x"]
                y = picture["objects"][i]["relative_coordinates"]["center_y"]
                w = picture["objects"][i]["relative_coordinates"]["width"]
                h = picture["objects"][i]["relative_coordinates"]["height"]
                
                image = cvDrawBoxes(x*width,y*height,w*width,h*height,image, picture["objects"][i]["confidence"])
            retval, buffer = cv2.imencode('.jpeg', image)
            jpg_as_text = base64.b64encode(buffer)
            base64_string = jpg_as_text.decode('utf-8')
            picts.append((picture["filename"], "data:image/jpeg;base64," + base64_string))
        #print(picts[0])
        return {"Pictures":picts}
        # print(number)
        # path = "X:/Frederik/fishy-stuff/scripts/pictures/Unverified"
        # files = sorted(os.listdir(path))
        # filename = files[int(number)] 
        # image = cv2.imread(path + "/" + filename)

        # for i in range(len(picturesWithFish)):
        #     if filename == picturesWithFish[i]["filename"].split("/")[-1]:
        #         for i in range(len(picturesWithFish[i]["objects"])):
        #             x = picturesWithFish[i]["objects"][i]["relative_coordinates"]["center_x"]
        #             y = picturesWithFish[i]["objects"][i]["relative_coordinates"]["center_y"]
        #             w = picturesWithFish[i]["objects"][i]["relative_coordinates"]["width"]
        #             h = picturesWithFish[i]["objects"][i]["relative_coordinates"]["height"]
        #             image = cvDrawBoxes(x*width,y*height,w*width,h*height,image)

if __name__ == "__main__":
    # Create a copy of the json results with only pictures that are predicted to have a fish
    # a = []
    # with open("/work1/s154227/videos/result_green_copy.json") as f:
    #     a = json.load(f)
    # print(len(a))
    # for i in range(len(a)):
    #     if len(a[i]["objects"]) > 0:
    #         picturesWithFish.append(a[i])
    # print("Removed all")
    # print(len(picturesWithFish))
    # with open('resultSimonFishDetected_v3.json', 'w') as json_file:
    #     json.dump(picturesWithFish, json_file)
    
    with open(pathasa) as f:
        picturesWithFish = json.load(f)

    with open(backgroundSpath) as f:
        backgroundS = json.load(f)
    
    with open(correctLabelingSpath) as f:
        correctLabelingS = json.load(f)
    
    with open(unknownSpath) as f:
        unknownS = json.load(f)
    
    # counter = 0       
    # files = os.listdir(path)
    # truefiles = os.listdir(truePath)
    # falsefiles = os.listdir(falsePath)
    # for i in range(len(picturesWithFish)):
    #     if  picturesWithFish[i]["filename"].split("/")[-1] not in files \
    #         and picturesWithFish[i]["filename"].split("/")[-1] not in truefiles \
    #         and picturesWithFish[i]["filename"].split("/")[-1] not in falsefiles:
    #         shutil.copy("X:/"+ "/".join(picturesWithFish[i]["filename"].split("/")[3:6]), path)
    #         print( "X:/"+ "/".join(picturesWithFish[i]["filename"].split("/")[3:6]))
    #         counter = counter + 1
    
    # print(picturesWithFish)
    app.run(port=5955,debug=True)

