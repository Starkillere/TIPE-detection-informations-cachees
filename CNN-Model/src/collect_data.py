import os
import requests
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
from steganography import LSBSteganography, StyleTransferSteganography, EXIFSteganography, InvisiblePixelsSteganography

def download_imagenet_images(output_dir, num_images):
    """
    Télécharge des images depuis ImageNet et les enregistre dans le dossier spécifié.
    """
    # Exemple d'URL d'ImageNet (à adapter selon l'API ou la source utilisée)
    base_url = "http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n00000000"
    
    # Télécharger les URLs des images
    response = requests.get(base_url)
    image_urls = response.text.splitlines()
    
    # Télécharger les images
    for i, url in enumerate(image_urls[:num_images]):
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.save(os.path.join(output_dir, f"image_{i}.jpg"))
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image {url}: {e}")

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