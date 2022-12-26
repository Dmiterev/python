import torch.nn as nn
import torch
import torch.optim as optim
from torchvision import datasets, models, transforms
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from PIL import Image
from sklearn.model_selection import train_test_split
import random

lr = 0.001
batch_size = 100
epochs = 10

device = 'cuda' if torch.cuda.is_available() else 'cpu'

torch.manual_seed(1234)
if device == 'cuda':
    torch.cuda.manual_seed_all(1234)


class dataset(torch.utils.data.Dataset):
    def __init__(self, file_list, transform=None, path=None):
        self.file_list = file_list
        self.transform = transform
        self.path = path

    def __len__(self):
        self.filelength = len(self.file_list)
        return self.filelength

    def __getitem__(self, idx):
        img_path = self.file_list[idx]
        img = Image.open(img_path)
        img_transformed = self.transform(img.convert("RGB"))
        label = img_path.split('/')[-1].split('.')[0]
        if label == os.path.join(self.path, "tiger"):
            label = 1
        elif label == os.path.join(self.path, "leopard"):
            label = 0
        return img_transformed, label


class Cnn(nn.Module):
    def __init__(self):
        super(Cnn, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.fc1 = nn.Linear(3 * 3 * 64, 10)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(10, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.view(out.size(0), -1)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)
        return out


def training_network(images_list: list) -> pd.DataFrame:
    """
    Создает и обучает модель сверточной нейронной сети. Анализирует результаты, сохраняет их в result.csv и строит
    графики.
    :param images_list: Список изображений из датасета.
    """
    random_idx = np.random.randint(1, len(images_list), size=10)
    fig = plt.figure()
    i = 1
    for idx in random_idx:
        ax = fig.add_subplot(2, 5, i)
        img = Image.open(images_list[idx])
        plt.imshow(img)
        i += 1
        plt.axis('off')
    plt.show()

    class_labels = []
    for i in range(1000):
        class_labels.append(True)
    for i in range(1000):
        class_labels.append(False)

    train_list, train_test_val, train_val, test_val = train_test_split(images_list, class_labels, test_size=0.2, shuffle=True)
    test_list, val_list, test, val = train_test_split(train_test_val, test_val, test_size=0.5)

    train_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])

    test_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor()
    ])

    train_data = dataset(train_list, transform=train_transforms, path=os.path.join("D:\\", "dataset"))
    val_data = dataset(val_list, transform=test_transforms, path=os.path.join("D:\\", "dataset"))
    train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)
    val_loader = torch.utils.data.DataLoader(dataset=val_data, batch_size=batch_size, shuffle=True)

    model = Cnn().to(device)
    model.train()

    optimizer = optim.Adam(params=model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    accuracy_values = []
    loss_values = []
    val_accuracy_values = []
    val_loss_values = []
    for epoch in range(epochs):
        epoch_loss = 0
        epoch_accuracy = 0

        for data, label in train_loader:
            data = data.to(device)
            label = label.to(device)

            output = model(data)
            loss = criterion(output, label)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            acc = ((output.argmax(dim=1) == label).float().mean())
            epoch_accuracy += acc / len(train_loader)
            epoch_loss += loss / len(train_loader)

        accuracy_values.append(float(epoch_accuracy))
        loss_values.append(float(epoch_loss))

        print('Epoch : {}, train accuracy : {}, train loss : {}'.format(epoch + 1, epoch_accuracy, epoch_loss))

        with torch.no_grad():
            epoch_val_accuracy = 0
            epoch_val_loss = 0
            for data, label in val_loader:
                data = data.to(device)
                label = label.to(device)

                val_output = model(data)
                val_loss = criterion(val_output, label)

                acc = ((val_output.argmax(dim=1) == label).float().mean())
                epoch_val_accuracy += acc / len(val_loader)
                epoch_val_loss += val_loss / len(val_loader)
            val_accuracy_values.append(float(epoch_val_accuracy))
            val_loss_values.append(float(epoch_val_loss))
            print('Epoch : {}, val_accuracy : {}, val_loss : {}'.format(epoch + 1, epoch_val_accuracy, epoch_val_loss))

    plt.figure(figsize=(15, 5))
    plt.plot(range(len(accuracy_values)), accuracy_values, color="green")
    plt.plot(range(len(val_accuracy_values)), val_accuracy_values, color="red")
    plt.legend(["Train accuracy", "Valid accuracy"])
    plt.show()

    plt.figure(figsize=(15, 5))
    plt.plot(range(len(loss_values)), [float(value) for value in loss_values], color="blue")
    plt.plot(range(len(val_loss_values)), [float(value) for value in val_loss_values], color="orange")
    plt.legend(["Train loss", "Valid loss"])
    plt.show()

    idx = []
    prob = []
    for i in range(len(accuracy_values)):
        idx.append(i)
        prob.append(accuracy_values[i])
    submission = pd.DataFrame({'id': idx, 'label': prob})
    submission.to_csv('result.csv', index=False)
    return submission


if __name__ == '__main__':
    images_list = glob.glob(os.path.join("D:\\", "dataset", '*.jpg'))
    submission = training_network(images_list)
    id_list = []
    class_ = {0: "tiger", 1: "leopard"}
    fig, axes = plt.subplots(2, 5, figsize=(20, 12), facecolor='w')
    for ax in axes.ravel():
        i = random.choice(submission['id'].values)
        class_random = random.choice(["tiger", "leopard"])
        label = submission.loc[submission['id'] == i, 'label'].values[0]
        if label > 0.5:
            label = 1
        else:
            label = 0
        img_path = os.path.join("D:\\", "dataset", f'{class_random}.{i:04d}.jpg')
        img = Image.open(img_path)
        plt.imshow(img)
        plt.axis("off")
        plt.suptitle(class_random)
        plt.show()