# Navigating repository


# YOLO
Darknet has been added as a git submodule. Make sure the darknet submodule is downloaded:

    $ git submodule init

To compile darknet on the HPC, use the following command from within this folder:

    $ ./compile_darknet.sh

## Training
To train a network using the HPC, queue up for use with 2 graphics cards using:

    $ bsub < queueYolo

This can also be called directly, if using an interactive node:

    $ ./queueYolo


## Inference

To perform inference on all the extracted images from all the videos, queue up using:

    $ bsub < queueYolo_inference

or from an interactive node:

    $ ./queueYolo_inference

## mAP

To calculate the mean average precision on the validation set, call:

    $ ./queueYolo_map