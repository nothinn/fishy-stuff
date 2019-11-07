import glob
import os
import torch
from PIL import Image
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms

image_paths = glob.glob('../extracted')
len(image_paths)

class Fishy(torch.utils.data.Dataset):
    """
    Description of fishy class

    Attributes:
        train : Percentage of set used for training.
        transform : 
        data_path : Path to images
    """

    def __init__(self, train, transform, data_path='../extracted', category_path="../all_fish.txt"):
        """
        Constructor for Fishy class

            Parameters:
                train : Percentage of set used for training.
                transform : 
                data_path : Path to images
        """
        self.transform = transform
        data_path = os.path.join(data_path, 'train' if train else 'test')
        fp = open(category_path, 'r')
        self.fish_dict =  {i.split(";")[0] : i.split(";")[1][1:-1] for i in fp}
        
        #self.name_to_label = [i.split(";")[1][1:-1] for i in fp]
        self.image_paths = glob.glob(data_path + '/*.jpg')
        
    def __len__(self):
        """
        Returns the total number of samples
        Returns :
            int : The total number of images
        """
        return len(self.image_paths)

    def __getitem__(self, idx):
        """
        Generates one sample of data

        Parameters:
            idx (int): Index for image

        Returns :
            Image : Transformed image.
        """
        image_path = self.image_paths[idx]
        
        lookup = image_path.split("/")[-1].split(".")[0]
        
        image = Image.open(image_path)
        #y = self.name_to_label[idx]
        y = self.fish_dict[lookup]
        X = self.transform(image)
        return X,y



#For testing
if False:
    batch_size = 32
    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5),
                            (0.5, 0.5, 0.5))]
    )

    trainset = Fishy(train=True, transform=transform)
    testset = Fishy(train=False, transform=transform)

    print(trainset[120])
    print(set(trainset.name_to_label))
