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
import torchvision

image_paths = glob.glob('../../../extracted')
len(image_paths)

fishies = {"p virens" : 0, "g morhua": 1, "h lanceolatus" : 2, "background" : 3}

class Fishy(torch.utils.data.Dataset):
    """
    Description of fishy class

    Attributes:
        train : Percentage of set used for training.
        transform : 
        data_path : Path to images
    """

    def __init__(self, train, transform, data_path='../../../extracted', category_path="../all_fish.txt"):
        """
        Constructor for Fishy class

            Parameters:
                train : Percentage of set used for training.
                transform : 
                data_path : Path to images
        """
        self.transform = transform
        #data_path = os.path.join(data_path, 'train' if train else 'test')
        fp = open(category_path, 'r')
        #i.split(";")[1][1:-1]

        #self.fish_dict =  {i.split(";")[0] : fishies[i.split(";")[1][1:-1]] for i in fp}
        self.fish_dict = {}
        count_categories = 0
        for i in fp:
            if self.fish_dict.get(fishies[i.split(";")[1][1:-1]]):
                self.fish_dict[fishies[i.split(";")[1][1:-1]]].append(i.split(";")[0])
            else:
                self.fish_dict[fishies[i.split(";")[1][1:-1]]] = [i.split(";")[0]]
                count_categories+=1
        
        self.mostPicturesSameCat = max([len(v) for k,v in self.fish_dict.items()])
        self.lengthOfArray = self.mostPicturesSameCat * count_categories
        #self.name_to_label = [i.split(";")[1][1:-1] for i in fp]
        self.image_paths = glob.glob(data_path + '/*.jpg')
        
    def __len__(self):
        """
        Returns the total number of samples
        Returns :
            int : The total number of images
        """
        return self.lengthOfArray

    def __getitem__(self, idx):
        """
        Generates one sample of data

        Parameters:
            idx (int): Index for image

        Returns :
            Image : Transformed image.
        """

        category = idx//self.mostPicturesSameCat

        pictures = self.fish_dict[category]
        idLookup = idx - self.mostPicturesSameCat * category
        picture = pictures[idLookup % len(pictures)]

        image_path = "../../../extracted/" + picture + ".jpg" #self.image_paths[idx] 
        
        #lookup = image_path.split("/")[-1].split(".")[0]
        
        image = Image.open(image_path)
        #y = self.name_to_label[idx]
        #y = self.fish_dict[lookup]
        X = self.transform(image)
        return X,category

def createDataLoaders(batch_size, size,rotation = 45, train_distribution = 0.8):
    #For testing
    transform = transforms.Compose(
        [transforms.Resize((size,size)),
        transforms.RandomRotation(rotation),
        transforms.RandomVerticalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5),
                            (0.5, 0.5, 0.5))]
    )
    full_dataset = Fishy(train=True, transform=transform)
    train_size = int(train_distribution * len(full_dataset))
    test_size = len(full_dataset) - train_size
    trainset, testset = torch.utils.data.random_split(full_dataset, [train_size, test_size])
    #trainset = Fishy(train=True, transform=transform)
    #testset = Fishy(train=False, transform=transform)
    train_loader = DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=6)
    test_loader = DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=6)

    return train_loader, test_loader, trainset, testset
'''
transform = transforms.Compose(
        [transforms.Resize((50,50)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5),
                            (0.5, 0.5, 0.5))]
    )
trainset = Fishy(train=True, transform=transform)
testset = Fishy(train=False, transform=transform)
train_loader = DataLoader(trainset, batch_size=16, shuffle=True, num_workers=3)
test_loader = DataLoader(testset, batch_size=16, shuffle=False, num_workers=3)
train_data_iter = iter(train_loader)
test_data_iter = iter(test_loader)



images, labels = train_data_iter.next()

print(labels)
'''
