"""
    Par Ayouba Anrezki
    le 2/01/2025
"""

from PIL import Image
import numpy as np
from PIL.ExifTags import TAGS

class LSBSteganography:
    @staticmethod
    def hide_text(image_path, output_path, text):
        """
        Cache un texte dans les bits de moindre poids (LSB) d'une image.
        """
        image = Image.open(image_path)
        pixels = np.array(image)
        
        # Convertir le texte en binaire
        binary_text = ''.join(format(ord(char), '08b') for char in text)
        text_length = len(binary_text)
        
        # Cacher le texte dans les LSB
        idx = 0
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                for k in range(3):  # Pour chaque canal (R, G, B)
                    if idx < text_length:
                        pixels[i, j, k] = (pixels[i, j, k] & ~1) | np.int8(binary_text[idx])
                        idx += 1
                    else:
                        break
        
        # S'assurer que les valeurs des pixels restent dans la plage 0-255
        pixels = np.clip(pixels, 0, 255).astype(np.uint8)
        
        # Sauvegarder l'image modifiée
        stego_image = Image.fromarray(pixels)
        stego_image.save(output_path)

    @staticmethod
    def hide_image(cover_path, output_path, secret_path):
        """
        Cache une image dans les bits de moindre poids (LSB) d'une autre image.
        """
        cover_image = Image.open(cover_path)
        secret_image = Image.open(secret_path).resize(cover_image.size)
        
        cover_pixels = np.array(cover_image)
        secret_pixels = np.array(secret_image)
        
        # Cacher l'image secrète dans les LSB
        for i in range(cover_pixels.shape[0]):
            for j in range(cover_pixels.shape[1]):
                for k in range(3):
                    cover_pixels[i, j, k] = (cover_pixels[i, j, k] & ~1) | ((secret_pixels[i, j, k] >> 7) & 1)
        
        # S'assurer que les valeurs des pixels restent dans la plage 0-255
        cover_pixels = np.clip(cover_pixels, 0, 255).astype(np.uint8)
        
        # Sauvegarder l'image modifiée
        stego_image = Image.fromarray(cover_pixels)
        stego_image.save(output_path)

class StyleTransferSteganography:
    @staticmethod
    def hide_image(cover_path, output_path, secret_path):
        """
        Cache une image dans une autre en utilisant un transfert de style.
        """
        # Implémentation simplifiée (à compléter avec un modèle de transfert de style)
        cover_image = Image.open(cover_path)
        secret_image = Image.open(secret_path).resize(cover_image.size)
        
        # Fusionner les images (exemple simplifié)
        stego_image = Image.blend(cover_image, secret_image, alpha=0.5)
        stego_image.save(output_path)

class EXIFSteganography:
    @staticmethod
    def hide_text(image_path, output_path, text):
        """
        Cache un texte dans les métadonnées EXIF d'une image.
        """
        image = Image.open(image_path)
        exif_data = image.getexif()
        
        # Ajouter le texte dans les métadonnées
        exif_data[0x9286] = text  # 0x9286 est le tag pour UserComment
        
        # Sauvegarder l'image avec les nouvelles métadonnées
        image.save(output_path, exif=exif_data)

class InvisiblePixelsSteganography:
    @staticmethod
    def hide_text(image_path, output_path, text):
        """
        Cache un texte en modifiant certains pixels de l'image.
        """
        image = Image.open(image_path)
        pixels = np.array(image)
        
        # Convertir le texte en binaire
        binary_text = ''.join(format(ord(char), '08b') for char in text)
        text_length = len(binary_text)
        
        # Cacher le texte dans les pixels marginaux
        idx = 0
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                if i < 10 or j < 10:  # Zone marginale
                    for k in range(3):
                        if idx < text_length:
                            pixels[i, j, k] = (pixels[i, j, k] & ~1) | int(binary_text[idx])
                            idx += 1
                        else:
                            break
        
        # S'assurer que les valeurs des pixels restent dans la plage 0-255
        pixels = np.clip(pixels, 0, 255).astype(np.uint8)
        
        # Sauvegarder l'image modifiée
        stego_image = Image.fromarray(pixels)
        stego_image.save(output_path)