from PIL import Image, ImageDraw

import json

with open("/work1/s154227/videos/result_first_500.json") as file:
	dict_first = json.load(file)
with open("/work1/s154227/videos/result_second_500.json") as file:
	dict_second = json.load(file)

for i in range(500):
	if len(dict_first[i]["objects"]) > 0 or len(dict_second[i]["objects"]) > 0:
		path = dict_first[i]["filename"]
		im = Image.open(path)
		draw = ImageDraw.Draw(im)
		for obj in dict_first[i]["objects"]:
			coor = obj["relative_coordinates"]
			x0 = 1280 * coor["center_x"] - 1280*(float(coor["width"])/2)
			x1 = 1280 * coor["center_x"] + 1280*(float(coor["width"])/2)
			y0 = 720 * coor["center_y"] - 720*float(coor["height"])/2
			y1 = 720 * coor["center_y"] + 720*float(coor["height"])/2
			draw.rectangle((x0,y0,x1,y1), outline = (255,0,0))
			draw.text((x0, y1),str(obj["confidence"]), fill = (255,0,0) )
		for obj in dict_second[i]["objects"]:
			coor = obj["relative_coordinates"]
			x0 = 1280 * coor["center_x"] - 1280*float(coor["width"])/2
			x1 = 1280 * coor["center_x"] + 1280*float(coor["width"])/2
			y0 = 720 * coor["center_y"] - 720*float(coor["height"])/2
			y1 = 720 * coor["center_y"] + 720*float(coor["height"])/2
			draw.rectangle((x0+2,y0+2,x1+2,y1+2), outline = (0,0,255))
			draw.text((x0, y1),str(obj["confidence"]), fill = (0,0,255) )
		im.save(path.split("/")[-1])
