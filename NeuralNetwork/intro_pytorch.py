import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from matplotlib import pyplot as plt
from torchvision import datasets, transforms

# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_data_loader(training = True):

    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    train_set = datasets.FashionMNIST('./data', train = True, download = True, transform = custom_transform)
    test_set = datasets.FashionMNIST('./data', train = False, transform = custom_transform)
    if training == True:
        return torch.utils.data.DataLoader(train_set, batch_size=64)
    else:
        return torch.utils.data.DataLoader(test_set, batch_size=64, shuffle = False)

def build_model():

    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(784, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 10)
    )
    return model


def train_model(model, train_loader, criterion, T):

    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()
    for epoch in range(T):
        total = 0
        accuracy = 0
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            prob, name = data
            opt.zero_grad()
            out = model(prob)
            loss = criterion(out, name)
            loss.backward()
            opt.step()
            _, predicted = torch.max(out.data, 1)
            accuracy += (predicted == name).sum().item()
            running_loss += loss.item() * 64
            total += name.size(0)
        print(f'Train Epoch: {epoch}\tAccuracy: {accuracy}/{total}({(accuracy*100)/total:.2f}%)\tLoss: {running_loss/total:.3f}')

def evaluate_model(model, test_loader, criterion, show_loss = True):

    total = 0
    accuracy = 0
    running_loss = 0.0
    model.eval()
    with torch.no_grad():
        for data in test_loader:
            pic, name = data
            out = model(pic)
            _, predicted = torch.max(out.data, 1)
            accuracy += (predicted == name).sum().item()
            loss = criterion(out, name)
            total += name.size(0)
            running_loss += loss.item() * 64
        if show_loss == True:
            print(f'Average loss: {running_loss / total:.4f}\nAccuracy: {(accuracy * 100) / total:.2f}%')
        else:
            print(f'Accuracy: {(accuracy * 100) / total}%')

def predict_label(model, test_images, index):
    names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag',
                   'Ankle Boot']

    logits = model(test_images[index])
    prob = F.softmax(logits, dim=1)
    prob_list = prob.tolist()
    dic = {}
    for i in range(len(names)):
        dic[names[i]] = prob_list[0][i]
    prediction = dict(dic)
    sorted_prediction = sorted(prediction.items(), key=lambda a: a[1], reverse=True)[:3]
    for k,v in sorted_prediction:
        print(f'{k}: {v * 100:.2f}%')
