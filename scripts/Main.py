import Network
import newLoader
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import numpy as np
import torch

from tqdm import tqdm

device = 'cuda' if torch.cuda.is_available() else 'cpu'

print("Using device: " + device)

height, width = 512, 512
num_classes   = 4

channels        = 3        
kernel_size     = 3
conv_stride     = 1
conv_pad        = 1
conv_drop_rate  = 0.4
image_size      = 64

network = Network.Net(channels, kernel_size,conv_stride, conv_pad, conv_drop_rate, num_classes, image_size)
print(network)
network.to(device)
LEARNING_RATE = 0.00001
criterion = nn.CrossEntropyLoss()

# weight_decay is equal to L2 regularization
optimizer = optim.Adam(network.parameters(), lr=LEARNING_RATE)

#training loop:

num_epoch = 50
batch_size = 64

trainingloader, testloader, trainset, testset = newLoader.createDataLoaders(batch_size, image_size)
train_acc_all = []
test_acc_all = []
try:
    for epoch in tqdm(range(num_epoch)):
        running_loss = 0.0
        train_correct = 0
        for i, data in enumerate(trainingloader, 0):

            inputs, labels = data
            inputs, labels = Variable(inputs).to(device), Variable(labels).to(device)

            optimizer.zero_grad()

            optimizer

            outputs = network(inputs)

            loss = criterion(outputs, labels)
            loss.backward()

            optimizer.step()

            running_loss += loss

            predicted = outputs.argmax(1)
            train_correct += (labels==predicted).sum().cpu().item()
            
            if i % 100 == 1:
                print("[%d, %5d] loss: %.3f" % 
                    (epoch + 1, i + 1, running_loss/1000))
                running_loss = 0.0
        
        network.eval()
        test_correct = 0.0
        for data, target in testloader:
            data = data.to(device)
            with torch.no_grad():
                output = network(data)
            predicted = output.argmax(1).cpu()
            test_correct += (target==predicted).sum().item()
        train_acc = train_correct/len(trainset)
        test_acc = test_correct/len(testset)
        train_acc_all.append(train_acc)
        test_acc_all.append(test_acc)
        print("Accuracy train: {train:.1f}%\t test: {test:.1f}%".format(test=100*test_acc, train=100*train_acc))
except(KeyboardInterrupt):
    print("Model saved")
    torch.save(network, "model.pt")
    
print("training over")

torch.save(network, "model.pt")

print("Saved model")