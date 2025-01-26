#-*- encoding:utf-8 -*-

"""colecte des caractèristiques"""

"""Par Ayouba Anrezki """

 # IMPORTATIONS DÉPENDENCES


import os
import numpy as np
from skimage.measure import shannon_entropy
from PIL import Image
from scipy.stats import chi2

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
def get_entropy(file_path):
    """
    Retourne l'entropie de Shannon.
    """
    try:
        img = Image.open(file_path)
        img = np.array(img)
        return shannon_entropy(img)
    except Exception as e:
        print(f"Erreur dans le calcul de l'entropie pour {file_path}: {e}")
        return None

# --- Densité des zéros ---
def get_zero_density(file_path):
    """
    Retourne la densité des zéros dans les données brutes.
    """
    try:
        
        img = Image.open(file_path)
        img = np.array(img).flatten()
        return np.sum(img == 0) / len(img)
    except Exception as e:
        print(f"Erreur dans le calcul de la densité des zéros pour {file_path}: {e}")
        return None

# --- Densité des uns ---
def get_one_density(file_path):
    """
    Retourne la densité des uns ou des pixels ayant la valeur maximale.
    """
    try:
        img = Image.open(file_path)
        img = np.array(img).flatten()
        return np.sum(img == 255) / len(img)
    except Exception as e:
        print(f"Erreur dans le calcul de la densité des uns pour {file_path}: {e}")
        return None

# --- Valeur moyenne ---
def get_mean_value(file_path):
    """
    Retourne la valeur moyenne des données.
    """
    try:
        img = Image.open(file_path)
        img = np.array(img).flatten()
        return np.mean(img)
    except Exception as e:
        print(f"Erreur dans le calcul de la valeur moyenne pour {file_path}: {e}")
        return None

# --- Écart-type ---
def get_std_dev(file_path):
    """
    Retourne l'écart-type des données.
    """
    try:
        img = Image.open(file_path)
        img = np.array(img).flatten()
        return np.std(img)
    except Exception as e:
        print(f"Erreur dans le calcul de l'écart-type pour {file_path}: {e}")
        return None

# --- Énergie moyenne ---
def get_energy(file_path):
    """
    Retourne l'énergie moyenne des données.
    """
    try:
        img = Image.open(file_path)
        img = np.array(img).flatten()
        return np.sum(img**2) / len(img)
    except Exception as e:
        print(f"Erreur dans le calcul de l'énergie pour {file_path}: {e}")
        return None

# --- Variance ---
def get_variance(file_path):
    """
    Retourne la variance des données.
    """
    try:
        img = Image.open(file_path)
        img = np.array(img).flatten()
        return np.var(img)
    except Exception as e:
        print(f"Erreur dans le calcul de la variance pour {file_path}: {e}")
        return None
    
def khi2(image_path: str) -> float:
    image = Image.open(image_path).convert("L")
    pixels = np.array(image).flatten()

    histogram, _ = np.histogram(pixels, bins=256, range=(0, 256))

    total_pixels = pixels.size
    expected = total_pixels / 256 

    chi_squared_stat = np.sum((histogram - expected) ** 2 / expected)

    p_value = 1 - chi2.cdf(chi_squared_stat, df=255)

    return p_value



def vraisemblance(image_path: str) -> float:
    image = Image.open(image_path).convert("L")
    pixels = np.array(image).flatten()

    histogram, _ = np.histogram(pixels, bins=256, range=(0, 256))

    total_pixels = pixels.size
    observed_prob = histogram / total_pixels

    uniform_prob = 1 / 256  

    log_likelihood = np.sum(histogram * np.log(observed_prob / uniform_prob + 1e-10))

    return log_likelihood

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
        "entropy": get_entropy(file_path),
        "zero_density": get_zero_density(file_path),
        "one_density": get_one_density(file_path),
        "mean_value": get_mean_value(file_path),
        "std_dev": get_std_dev(file_path),
        "energy": get_energy(file_path),
        "variance": get_variance(file_path),
        "khi2": khi2(file_path),
        "vraisemblance": vraisemblance(file_path)
    })
        
    for clean in cleans:

        file_type = "image" if clean.split(".")[-1] == "jpg" else "audio"
        file_path = f"{dir_clean}{clean}"

        features.append({
        "is_stego": 0,
        "file_size": get_file_size(file_path),
        "entropy": get_entropy(file_path),
        "zero_density": get_zero_density(file_path),
        "one_density": get_one_density(file_path),
        "mean_value": get_mean_value(file_path),
        "std_dev": get_std_dev(file_path),
        "energy": get_energy(file_path),
        "variance": get_variance(file_path),
        "khi2": khi2(file_path),
        "vraisemblance": vraisemblance(file_path)
    })

    return features