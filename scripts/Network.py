#Give other people read/write access to your files in a folder
# chmod -R g+rw <FOLDER>

import numpy as np
import os

from skimage.io import imread
from skimage.transform import resize

import sys
sys.path.append(os.path.join('.', '..')) # Allow us to import shared custom 
#                                         # libraries, like utils.py

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim



from torch.utils.data import DataLoader
'''
height, width = 512, 512
num_classes   = 4

channels        = 3        
kernel_size     = 3
conv_stride     = 1
conv_pad        = 1
conv_drop_rate  = 0.4
'''


class Net(nn.Module):
    def __init__(self, channels, kernel_size,conv_stride, conv_pad, conv_drop_rate, num_classes, image_size):
        super(Net, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels = channels, #3 channels
                out_channels = 16, 
                kernel_size = kernel_size, 
                stride = conv_stride, 
                padding = conv_pad),

            nn.BatchNorm2d(num_features = 16),

            nn.MaxPool2d(2),

            nn.ReLU(),

            nn.Dropout2d(p=conv_drop_rate),

            nn.Conv2d(in_channels = 16, 
                out_channels = 32, 
                kernel_size = kernel_size, 
                stride = conv_stride, 
                padding = conv_pad),

            nn.BatchNorm2d(num_features = 32),

            nn.ReLU(),

            nn.Dropout2d(p=conv_drop_rate),

            nn.Conv2d(in_channels = 32, 
                out_channels = 64, 
                kernel_size = kernel_size, 
                stride = conv_stride, 
                padding = conv_pad)

        )

        self.fc = nn.Sequential(
            nn.Linear(in_features = 64 * (image_size//2) * (image_size//2), out_features = 256, bias = True),
            
            #nn.BatchNorm1d(256),
            
            nn.ReLU(),

            nn.Linear(in_features = 256, out_features = num_classes, bias = False),

            nn.Softmax(dim = 1)
        )

    def forward(self, x):
        x_img = self.conv(x)
        x_img = x_img.view(x_img.shape[0],-1)
        
        out = self.fc(x_img)
        return out



#net = Net(channels, kernel_size,conv_stride, conv_pad, conv_drop_rate)
#print(net)




#Training loop:
