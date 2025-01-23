#-*- encoding:utf-8 -*-

"""Étude des caractèristiques"""

"""Par Ayouba Anrezki """

 # IMPORTATIONS DÉPENDENCES


import os
import numpy as np
from skimage.measure import shannon_entropy
from PIL import Image
import wave

__all__ = ["extract_all_features"]

 # paramètre globals

dir_clean =  "data/clean/"
dir_stego =  "data/stego/"

 # fonction d'extraction

# --- Taille du fichier ---
def get_file_size(file_path):
    """
    Retourne la taille du fichier en octets.
    """
    return os.path.getsize(file_path)

# --- Entropie ---
def get_entropy(file_path, file_type):
    """
    Retourne l'entropie de Shannon.
    """
    if file_type == "image":
        try:
            img = Image.open(file_path)
            img = np.array(img)
            return shannon_entropy(img)
        except Exception as e:
            print(f"Erreur dans le calcul de l'entropie pour {file_path}: {e}")
            return None
    elif file_type == "audio":
        try:
            with wave.open(file_path, 'rb') as audio_file:
                frames = audio_file.readframes(audio_file.getnframes())
                data = np.frombuffer(frames, dtype=np.int16)
                return shannon_entropy(data)
        except Exception as e:
            print(f"Erreur dans le calcul de l'entropie pour {file_path}: {e}")
            return None

# --- Densité des zéros ---
def get_zero_density(file_path, file_type):
    """
    Retourne la densité des zéros dans les données brutes.
    """
    try:
        if file_type == "image":
            img = Image.open(file_path)
            img = np.array(img).flatten()
            return np.sum(img == 0) / len(img)
        elif file_type == "audio":
            with wave.open(file_path, 'rb') as audio_file:
                frames = audio_file.readframes(audio_file.getnframes())
                data = np.frombuffer(frames, dtype=np.int16)
                return np.sum(data == 0) / len(data)
    except Exception as e:
        print(f"Erreur dans le calcul de la densité des zéros pour {file_path}: {e}")
        return None

# --- Densité des uns ---
def get_one_density(file_path, file_type):
    """
    Retourne la densité des uns ou des pixels ayant la valeur maximale.
    """
    try:
        if file_type == "image":
            img = Image.open(file_path)
            img = np.array(img).flatten()
            return np.sum(img == 255) / len(img)
        elif file_type == "audio":
            with wave.open(file_path, 'rb') as audio_file:
                frames = audio_file.readframes(audio_file.getnframes())
                data = np.frombuffer(frames, dtype=np.int16)
                return np.sum(data == 32767) / len(data)  # Max pour int16
    except Exception as e:
        print(f"Erreur dans le calcul de la densité des uns pour {file_path}: {e}")
        return None

# --- Valeur moyenne ---
def get_mean_value(file_path, file_type):
    """
    Retourne la valeur moyenne des données.
    """
    try:
        if file_type == "image":
            img = Image.open(file_path)
            img = np.array(img).flatten()
            return np.mean(img)
        elif file_type == "audio":
            with wave.open(file_path, 'rb') as audio_file:
                frames = audio_file.readframes(audio_file.getnframes())
                data = np.frombuffer(frames, dtype=np.int16)
                return np.mean(data)
    except Exception as e:
        print(f"Erreur dans le calcul de la valeur moyenne pour {file_path}: {e}")
        return None

# --- Écart-type ---
def get_std_dev(file_path, file_type):
    """
    Retourne l'écart-type des données.
    """
    try:
        if file_type == "image":
            img = Image.open(file_path)
            img = np.array(img).flatten()
            return np.std(img)
        elif file_type == "audio":
            with wave.open(file_path, 'rb') as audio_file:
                frames = audio_file.readframes(audio_file.getnframes())
                data = np.frombuffer(frames, dtype=np.int16)
                return np.std(data)
    except Exception as e:
        print(f"Erreur dans le calcul de l'écart-type pour {file_path}: {e}")
        return None

# --- Énergie moyenne ---
def get_energy(file_path, file_type):
    """
    Retourne l'énergie moyenne des données.
    """
    try:
        if file_type == "image":
            img = Image.open(file_path)
            img = np.array(img).flatten()
            return np.sum(img**2) / len(img)
        elif file_type == "audio":
            with wave.open(file_path, 'rb') as audio_file:
                frames = audio_file.readframes(audio_file.getnframes())
                data = np.frombuffer(frames, dtype=np.int16)
                return np.sum(data**2) / len(data)
    except Exception as e:
        print(f"Erreur dans le calcul de l'énergie pour {file_path}: {e}")
        return None

# --- Variance ---
def get_variance(file_path, file_type):
    """
    Retourne la variance des données.
    """
    try:
        if file_type == "image":
            img = Image.open(file_path)
            img = np.array(img).flatten()
            return np.var(img)
        elif file_type == "audio":
            with wave.open(file_path, 'rb') as audio_file:
                frames = audio_file.readframes(audio_file.getnframes())
                data = np.frombuffer(frames, dtype=np.int16)
                return np.var(data)
    except Exception as e:
        print(f"Erreur dans le calcul de la variance pour {file_path}: {e}")
        return None

def extract_all_features():
    """
    Extrait toutes les caractéristiques d'un fichier donné.
    :param file_path: Chemin du fichier
    :param file_type: Type de fichier ('image' ou 'audio')
    :return: Dictionnaire des caractéristiques
    """

    stegos =  [f for f in os.listdir(dir_stego) if os.path.isfile(os.path.join(dir_stego, f))]
    cleans =  [f for f in os.listdir(dir_clean) if os.path.isfile(os.path.join(dir_clean, f))]
    features =  []

    for stego in stegos:

        file_type = "image" if stego.split(".")[-1] == "jpg" else "audio"
        file_path = f"{dir_stego}{stego}"

        features.append({
        "is_stego": 1,
        "file_size": get_file_size(file_path),
        "entropy": get_entropy(file_path, file_type),
        "zero_density": get_zero_density(file_path, file_type),
        "one_density": get_one_density(file_path, file_type),
        "mean_value": get_mean_value(file_path, file_type),
        "std_dev": get_std_dev(file_path, file_type),
        "energy": get_energy(file_path, file_type),
        "variance": get_variance(file_path, file_type),
    })
        
    for clean in cleans:

        file_type = "image" if clean.split(".")[-1] == "jpg" else "audio"
        file_path = f"{dir_clean}{clean}"

        features.append({
        "is_stego": 0,
        "file_size": get_file_size(file_path),
        "entropy": get_entropy(file_path, file_type),
        "zero_density": get_zero_density(file_path, file_type),
        "one_density": get_one_density(file_path, file_type),
        "mean_value": get_mean_value(file_path, file_type),
        "std_dev": get_std_dev(file_path, file_type),
        "energy": get_energy(file_path, file_type),
        "variance": get_variance(file_path, file_type),
    })

    return features