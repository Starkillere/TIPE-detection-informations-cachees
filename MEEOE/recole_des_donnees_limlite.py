from math import *
import numpy as np
import sqlite3 as s3
from PIL import Image
import librosa
import cv2
from scipy.io import wavfile
from pydub import AudioSegment
from skimage.util import random_noise
from datetime import datetime
import random

def collect_cover_from_db(database: str) -> list[dict]:
    """
    Collecte les données de couverture depuis la base de données.

    Args:
        database (str): Chemin vers la base de données.

    Returns:
        list[dict]: Liste de dictionnaires représentant les données de couverture.
    """
    covers = []
    try:
        conn = s3.connect(database)
        cursor = conn.cursor()
        
        query = "SELECT id, path, type, id_hideDat FROM cover_data"
        for row in cursor.execute(query):
            covers.append({
                "id": row[0],
                "path": row[1],
                "type": row[2],
                "id_hideDat": row[3],
            })
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la collecte des données de couverture : {e}")
        exit(0)
    
    return covers

def collect_hote_data_from_db(database: str) -> list[dict]:
    """
    Collecte les données hôtes depuis la base de données.
    """
    hotes = []
    try:
        conn = s3.connect(database)
        cursor = conn.cursor()
        query = "SELECT id, path, type, methode, taille FROM hote_data"
        for row in cursor.execute(query):
            hotes.append({
                "id": row[0],
                "path": row[1],
                "type": row[2],
                "methode": row[3],
                "taille": row[4],
            })
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la collecte des données hôtes: {e}")
    return hotes


def entropie_desdonnes_cachees(cover:dict) -> float:
    entropy:float = 0.0
    match cover["type"]:
        case "img":
            image = Image.open(cover["path"]).convert("L")
            pixel_array = np.array(image)
            histograme, _ = np.histogram(pixel_array, bins=256, range=(0,256), density=True)
            histograme =  histograme[histograme > 0]
            entropy =  -np.sum(histograme*np.log2(histograme))

        case "son":
            signal, sr = librosa.load(cover["path"], sr=None, mono=True)
            signal_normalized = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
            histograme, _ = np.histogram(signal_normalized, bins=256, range=(0, 1), density=True)
            histograme = histograme[histograme > 0]
            entropy =  - np.sum(histograme*np.log2(histograme))
        
    return entropy

def variance_des_donnees_cachees(cover:dict) -> float:
    variance:float = 0.0
    match cover["type"]:
        case "img":
            image =  cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            mean = np.mean(image)
            variance = np.mean((image - mean) ** 2)
        case "son":
            signal, sr = librosa.load(cover["path"], sr=None, mono=True)
            signal_normalized = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
            mean = np.mean(signal_normalized)
            variance = np.mean((signal_normalized -mean) ** 2)
    return variance

def resitance_a_la_compression(cover:dict):
    psnr:float =  0.0
    pathfile:str =  f"delete/to_delete_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(0,99999999999)}{cover['path'][18:]}_."+cover["path"].split(".")[len(cover["path"].split("."))-1]
    match cover["type"]:
        case "img":
            res:float =  0.0
            compression_quality = 50
            image = cv2.imread(cover["path"])
            if image is None:
                raise FileNotFoundError(f"Unable to load image from path: {cover['path']}")

            cv2.imwrite(pathfile, image, [cv2.IMWRITE_JPEG_QUALITY, compression_quality])
            compressed_image =  cv2.imread(pathfile)
            mse = np.mean((image - compressed_image)**2)

            if mse == 0:
                return float("inf")
            max_pixel_value = 255.0
            psnr = 20 * np.log10(max_pixel_value/np.sqrt(mse))
        case "son":
            codec = cover["path"].split(".")[len(cover["path"].split("."))-1]
            bitrate =  "64k"

            audio = AudioSegment.from_file(cover["path"])
            original_samples = np.array(audio.get_array_of_samples())

            audio.export(pathfile, format=codec, bitrate=bitrate)
            compressed_audio =  AudioSegment.from_file(pathfile)
            compressed_samples =  np.array(compressed_audio.get_array_of_samples())

            min_length = min(len(original_samples), len(compressed_samples))
            original_samples = original_samples[:min_length]

            mse = np.mean((original_samples - compressed_samples)**2)

            signal_power = np.mean(original_samples ** 2)

            psnr = np.log10(signal_power/mse) if mse > 0 else float("inf")
    return psnr

def resitance_au_bruit(cover:dict):
    res = 0.0
    noise_type = "gaussian"
    noise_intensity = 0.01
    max_value = 255
    match cover["type"]:
        case "img":
            original_image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            noisy_image = random_noise(original_image, mode='gaussian', var=noise_intensity**2)
            noisy_image = (noisy_image * 255).astype(np.uint8)
            mse = np.mean((original_image - noisy_image) ** 2)
            psnr = 20 * log10(max_value / sqrt(mse)) if mse != 0 else float('inf')
            if psnr > 30:
                res = 2
            elif psnr > 20:
                res = 1
            else:
                res = 0
        case "son":
            sample_rate, original_audio = wavfile.read(cover["path"])
            if len(original_audio.shape) > 1:
                original_audio = original_audio[:, 0]
            noise = np.random.normal(0, noise_intensity * np.max(original_audio), original_audio.shape)
            noisy_audio = original_audio + noise
            noisy_audio = np.clip(noisy_audio, -32768, 32767).astype(np.int16)
            signal_power = np.mean(original_audio ** 2)
            noise_power = np.mean((original_audio - noisy_audio) ** 2)
            psnr = 10 * log10(signal_power / noise_power) if noise_power != 0 else float('inf')
            if psnr > 30:
                res = 2
            elif psnr > 20:
                res = 1
            else:
                res = 0
    return res

def data_collect(database: str) -> dict:
    """
    Collecte des métriques sur les données cachées dans les couvertures et les stocke dans une base de données.
    
    INPUT:
        database (str): Chemin vers la base de données SQLite.
        
    OUTPUT:
        dict: Une liste de dictionnaires contenant les métriques collectées.
    """
    covers = collect_cover_from_db(database) 
    datas = []
    
    conn = s3.connect(database)
    cursor = conn.cursor()

    for cover in covers:
        data = {}
        data["id_coverData"] = cover["id"]
        data["entropie_des_donnes_cachees"] = entropie_desdonnes_cachees(cover)
        data["variance_a_la_compression"] = variance_des_donnees_cachees(cover)
        data["resistance_a_la_compression"] = resitance_a_la_compression(cover)
        data["resistance_au_bruit"] = resitance_au_bruit(cover)
        datas.append(data)

        cursor.execute("""
            INSERT INTO data (
                id_coverData, 
                entropie_des_donnees_cachees, 
                variance_des_donnees_porteuses,
                resistance_a_la_compression, 
                resistance_au_bruit
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            data["id_coverData"],
            data["entropie_des_donnes_cachees"],
            data["variance_a_la_compression"],
            data["resistance_a_la_compression"],
            data["resistance_au_bruit"],
        ))

    conn.commit()
    conn.close()

    return datas


def data_collect_without_transformation(database: str) -> dict:

    covers = collect_hote_data_from_db(database) 
    datas = []
    
    conn = s3.connect(database)
    cursor = conn.cursor()

    for cover in covers:
        data = {}
        data["id_hote"] = cover["id"]
        data["entropie_des_donnes_cachees"] = entropie_desdonnes_cachees(cover)
        data["variance_a_la_compression"] = variance_des_donnees_cachees(cover)
        data["resistance_a_la_compression"] = resitance_a_la_compression(cover)
        data["resistance_au_bruit"] = resitance_au_bruit(cover)
        datas.append(data)

        cursor.execute("""
            INSERT INTO data_without_transformation (
                id_hote, 
                entropie_des_donnees_cachees, 
                variance_des_donnees_porteuses,
                resistance_a_la_compression, 
                resistance_au_bruit
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            data["id_hote"],
            data["entropie_des_donnes_cachees"],
            data["variance_a_la_compression"],
            data["resistance_a_la_compression"],
            data["resistance_au_bruit"],
        ))

    conn.commit()
    conn.close()

    return datas