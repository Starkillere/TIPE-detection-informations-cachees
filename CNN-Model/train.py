"""
    Par Ayouba Anrezki
    le 2/01/2025
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from models.cnn import StegoCNN

# Définir un dataset personnalisé
class StegoDataset(Dataset):
    def __init__(self, clean_dir, stego_dir, transform=None):
        self.clean_images = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.jpg')]
        self.stego_images = [os.path.join(stego_dir, f) for f in os.listdir(stego_dir) if f.endswith('.jpg')]
        self.all_images = self.clean_images + self.stego_images
        self.labels = [0] * len(self.clean_images) + [1] * len(self.stego_images)  # 0 = clean, 1 = stego
        self.transform = transform
    
    def __len__(self):
        return len(self.all_images)
    
    def __getitem__(self, idx):
        image_path = self.all_images[idx]
        image = Image.open(image_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

# Transformations pour les images
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalisation pour ImageNet
])

clean_dir = 'data/clean'
stego_dir = 'data/stego'

# Créer le dataset et le DataLoader
dataset = StegoDataset(clean_dir, stego_dir, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Initialiser le modèle, la fonction de perte et l'optimiseur
model = StegoCNN()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Entraînement du modèle
num_epochs = 10
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(dataloader):
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        
        if (i + 1) % 100 == 0:
            print(f"Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{len(dataloader)}], Loss: {loss.item():.4f}")
    
    print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / len(dataloader):.4f}")

# Sauvegarder le modèle entraîné
torch.save(model.state_dict(), 'models/stego_cnn.pth')
print("Modèle entraîné et sauvegardé.")