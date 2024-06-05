import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# Configuration des hyperparamètres
batch_size = 128
learning_rate = 0.001
num_epochs = 20

# Préparation des transformations des données
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(36, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

# Chargement des données CIFAR-10
# TODO: changer ./data
train_dataset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform, persistent_workers=True, pin_memory=True, prefetch_factor=8, num_workers=8)
test_dataset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform, persistent_workers=True, pin_memory=True, prefetch_factor=8, num_workers=8)

# Chargement des données avec DataLoader
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# Définition du modèle
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 36, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(36, 72, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(72, 126, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(126 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        
        x = self.conv3(x)
        x = self.relu(x)
        x = self.pool(x)
        
        x = x.view(-1, 126 * 4 * 4)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

model = SimpleCNN()
model.cuda()
# Initialisation des poids (par défaut)
# Pas de fonction spécifique d'initialisation des poids

# Optimiseur
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

# Fonction de coût
criterion = nn.CrossEntropyLoss()

# Entraînement du modèle
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.cuda(), labels.cuda()
        
        optimizer.zero_grad()
        
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        if i % 100 == 99:  # Print every 100 batches
            print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{len(train_loader)}], Loss: {running_loss / 100:.4f}')
            running_loss = 0.0
    
    # Pas de scheduler de taux d'apprentissage

    # Évaluation du modèle
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.cuda(), labels.cuda()
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    print(f'Accuracy of the model on the test images: {100 * correct / total:.2f}%')

print('Finished Training')