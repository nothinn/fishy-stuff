
import json 
import tensorflow as tf
import numpy as np
import imageio
import os.path

fpout = open("/work1/s154227/videos/detections.json", "w")
fpout.write("[\n")
with open("/work1/s154227/videos/detections.txt") as fp:
        line = fp.readline()[:-1]
        cnt = 1
        while line:
            print(cnt)
            fishes = line.split(";")
            filepath = fishes[0].split(":")
            fpout.write("{\n")
            fpout.write("\"frame_id\":" + str(cnt) + ",\n")
            fpout.write("\"filename\":\""+ filepath[0] +"\",\n")
            fpout.write("\"objects\": [\n")
            if len(fishes) > 1:
                for i in range(1, len(fishes)):
                    current = fishes[i].split(" fish")
                    fishsplit = current[0].split(":")
                    scString = fishsplit[1].split(" ")
                    box = fishsplit[2][2:-1].split(" ")
                    y0 = float(box[0][:-1])/720
                    y1 = float(box[2][:-1])/720
                    x0 = float(box[1][:-1])/1280
                    x1 = float(box[3])/1280
                    height = y1 - y0
                    width = x1 - x0   
                    cx = x0 + width/2
                    cy = y0 + height/2
                    fpout.write("{\"class_id\":0, \"name\":\"fish\", \"relative_coordinates\":{\"center_x\":"+ str(cx) +", \"center_y\":" + str(cy) +", \"width\":" + str(width) + ", \"height\":" + str(height) + "}, \"confidence\":" + scString[1] +"}")
                    if i != len(fishes)-1:
                        fpout.write(",")
                    fpout.write("\n")
            fpout.write("]\n")
            fpout.write("},\n")


            cnt += 1                
            line = fp.readline()[:-1]
fpout.write("]")
print("done")
fpout.close()


