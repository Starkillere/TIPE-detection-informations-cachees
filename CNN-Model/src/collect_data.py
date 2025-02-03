"""
    Par Ayouba Anrezki
    le 2/01/2025
"""

import os
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from PIL import Image
from .steganography import LSBSteganography, StyleTransferSteganography, EXIFSteganography, InvisiblePixelsSteganography

def download_images(output_dir, num_images, dataset_name="CIFAR10"):
    """
    Télécharge des images depuis un dataset prédéfini (comme CIFAR-10) et les enregistre dans le dossier spécifié.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Choix du dataset
    if dataset_name == "CIFAR10":
        dataset = datasets.CIFAR10(root='./data', download=True, transform=transforms.ToTensor())
    elif dataset_name == "CIFAR100":
        dataset = datasets.CIFAR100(root='./data', download=True, transform=transforms.ToTensor())
    else:
        raise ValueError("Dataset non supporté. Utilisez 'CIFAR10' ou 'CIFAR100'.")
    
    # Sauvegarder les images
    for i in range(min(num_images, len(dataset))):
        image, _ = dataset[i]  # Ignorer les étiquettes
        image = transforms.ToPILImage()(image)
        image.save(os.path.join(output_dir, f"image_{i}.jpg"))

def apply_steganography(input_dir, output_dir, num_stego_images):
    """
    Applique les méthodes de stéganographie sur les images de couverture.
    """
    image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]
    for i, image_file in enumerate(image_files[:num_stego_images]):
        image_path = os.path.join(input_dir, image_file)
        output_path = os.path.join(output_dir, f"stego_{i}.jpg")
        
        # Appliquer différentes méthodes de stéganographie
        if i % 5 == 0:
            LSBSteganography.hide_text(image_path, output_path, "Ceci est un message secret")
        elif i % 5 == 1:
            LSBSteganography.hide_image(image_path, output_path, "path_to_hidden_image.jpg")
        elif i % 5 == 2:
            StyleTransferSteganography.hide_image(image_path, output_path, "path_to_hidden_image.jpg")
        elif i % 5 == 3:
            EXIFSteganography.hide_text(image_path, output_path, "Ceci est un message secret")
        elif i % 5 == 4:
            InvisiblePixelsSteganography.hide_text(image_path, output_path, "Ceci est un message secret")

def resize_images(image_dir, size):
    """
    Redimensionne toutes les images dans le dossier spécifié.
    """
    for image_file in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_file)
        image = Image.open(image_path)
        image = image.resize(size)
        image.save(image_path)