import os
from src.collect_data import download_imagenet_images, apply_steganography, resize_images

def main():
    # Chemins des dossiers
    raw_dir = 'data/raw'
    clean_dir = 'data/clean'
    stego_dir = 'data/stego'
    
    # Créer les dossiers s'ils n'existent pas
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(clean_dir, exist_ok=True)
    os.makedirs(stego_dir, exist_ok=True)
    
    # Télécharger les images depuis ImageNet
    print("Téléchargement des images clean...")
    download_imagenet_images(clean_dir, num_images=30000)
    
    print("Téléchargement des images de couverture...")
    download_imagenet_images(raw_dir, num_images=20000)
    
    # Appliquer les méthodes de stéganographie
    print("Application des méthodes de stéganographie...")
    apply_steganography(raw_dir, stego_dir, num_stego_images=10000)
    
    # Redimensionner les images
    print("Redimensionnement des images...")
    resize_images(clean_dir, (256, 256))
    resize_images(stego_dir, (256, 256))
    
    print("Préparation des données terminée.")

if __name__ == "__main__":
    main()