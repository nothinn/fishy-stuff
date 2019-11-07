
import torch
import newLoader

device = 'cuda' if torch.cuda.is_available() else 'cpu'

network = torch.load("model.pt")

network.to(device)

network.eval()

trainloader, testloader, trainset, testset = newLoader.createDataLoaders(3000,64)

test_iter = iter(testloader)

images, labels = next(test_iter)
outputs = network(images.to(device))
predicted = outputs.argmax(1).cpu()

for i in range(len(predicted)):
    if predicted[i] != labels[i]:
        print("Predicted {} the true label {}".format(predicted[i], labels[i]))
