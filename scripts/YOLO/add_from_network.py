import json

with open("../pictures/backgroundS.json") as file:
	background = json.load(file)
with open("../pictures/correctLabelingS.json") as file:
	correct = json.load(file)


print(correct)


images = []

for detection in background:
	fileName = detection["filename"]
	images.append(fileName)
	
	fileName = fileName.split(".")[0] + ".txt"
	
	with open(fileName, "w") as file:
		for obj in detection["objects"]:
			cor = obj["relative_coordinates"]
			file.write("{} {} {} {} {}\n".format(obj["class_id"],cor["center_x"],cor["center_y"],cor["width"],cor["height"]))

for detection in correct:
	fileName = detection["filename"]
	images.append(fileName)
	
	fileName = fileName.split(".")[0] + ".txt"
	
	with open(fileName, "w") as file:
		print (fileName)
		for obj in detection["objects"]:
			cor = obj["relative_coordinates"]
			file.write("{} {} {} {} {}\n".format(obj["class_id"],cor["center_x"],cor["center_y"],cor["width"],cor["height"]))
	
	
	
with open("../../cfg/fish_green.data") as file:
	lines = file.readlines()
	for line in lines:
		if line.startswith("train"):
			pathToTrain = line.split(" ")[-1]
	
	
with open(pathToTrain.split()[0],"a") as file:
	for image in images:
		file.write(image + "\n")
		print(image)
