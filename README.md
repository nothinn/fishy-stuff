# Fishy-stuff
Project repository for 02456 - Deep Learning course at DTU.
- S154663 Anthon V. Riber
- S154227 Simon T. Andersen
- S153430 Frederik K. Drachmann
- S153427 Jacob H. Jessen


## Content
This README helps nagvigate the reposities content for the curious.

#### HandInNoteBook.ipynb
This is a notebook version of a CNN classifier which was designed during the project. This network is also found in .py files in the top folder of **/script** which can be trained running **/scripts/Main.py**

#### scipts/ExtractSquareImg
A script that uses labels from DTU aquas detection dataset and crop the images based on bounding boxes. Write new labels for training of classification network.

#### scripts/AlterF4KDataSet
A simple scrip to convert the labels from the Fish4Knowladge to a format that fint darknet detection training. This was needed at the F4K is made for classification not detection.

#### /Projekt _ Project
The content of this folder is what we used from the reference work by Peter Mørch Grot. 

**/Projekt _ Project/PredictImgList.py** feed our library of frames from DTU aquas videos, to Grot's network. It writes labels based on the predtions which are then used for the front end before being added to the expanded data-set.

**/Projekt _ Project/ConvertPredictToJson.py**  Converts label from PredictImgList run to JSON format used by darknet

**Projekt _ Project/s164049/cfg** contains the model by Peter Mørch Grot

**/scripts/API.py** The API that feeds images to the front end. Only images where fish are detected are shown send to the front end.
**/fishy-site** The front end for showing images. The front end is created in React. If node js is installed the front end can be run by doing "npm start" inside the "fishy-site" folder. The API then also has be started up the acutally get images.
