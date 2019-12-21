import tensorflow as tf
import numpy as np
import imageio
import os.path
def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it 
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

mygraph = load_graph("s164049/cfg/frozen_inference_graph.pb")

x = mygraph.get_tensor_by_name("prefix/image_tensor:0")
y0 = mygraph.get_tensor_by_name("prefix/detection_boxes:0")
y1 = mygraph.get_tensor_by_name("prefix/detection_scores:0")
y2 = mygraph.get_tensor_by_name("prefix/num_detections:0")


image = imageio.imread("/work1/s154227/Anthon/Projekt _ Project/GOPR2089.MP4_frame0311.jpg")
image = np.expand_dims(image, axis=0)

fpout = open("/work1/s154227/videos/detections.txt", "w")
with tf.Session(graph=mygraph) as sess:
    # Note: we don't nee to initialize/restore anything
    # There is no Variables in this graph, only hardcoded constants 
    with open("/work1/s154227/videos/imagelist.txt") as fp:
        line = fp.readline()[:-1]
        while line:
            if (os.path.isfile(line)):
                image = imageio.imread(line)
                image = np.expand_dims(image, axis=0)
                (y_numdect, y_scores, y_boxes ) = sess.run((y2, y1, y0), feed_dict={
                    x: image # < 45
                })
                fpout.write(line + ":")
                for i in range(int(y_numdect[0])):
                    fpout.write(" fish nr " + str(i) + "; certainty: " + str(y_scores[0, i]) + " box: (" + str(y_boxes[0, i, 0]*720) + ", " + str(y_boxes[0, i, 1]*1280) + ", " + str(y_boxes[0, i, 2 ]*720)+ ", " + str(y_boxes[0, i, 3]*1280)+ ")")
                fpout.write("\n")    
            
            line = fp.readline()[:-1]

fpout.close()

