from math import *
import numpy as np
import sqlite3 as s3
from PIL import Image
import librosa
import cv2
from scipy.stats import shapiro, normaltest
from scipy.io import wavfile
from pydub import AudioSegment
from skimage.util import random_noise
from scipy.signal import white_noise
from scipy.stats import chi2_contingency
from scipy.fft import fft, fft2
from scipy.signal import welch
from pywt import wavedec2
from scipy.linalg import lapack


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
    
    return covers


def entropie_desdonnes_cachees(cover:dict) -> float:
    entropy:float = 0.0
    match cover["type"]:
        case "img":
            image = Image.open(cover["path"]).convert("L")
            pixel_array = np.array(image)
            histogram, _ = np.histogram(pixel_array, bin=256, range=(0,256), density=True)
            histogram =  histogram[histogram > 0]
            entropy =  -np.sum(histogram*np.log2(histogram))

        case "son":
            signal, sr = librosa.load(cover["path"], sr=None, mono=True)
            signal_normalized = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
            histogram, _ = np.histogram(signal_normalized, bin=256, range=(0, 1), density=True)
            histogram = histogram[histogram > 0]
            entropy =  - np.sum(histogram*np.log2(histogram))
        
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

def test_de_normalite(cover:dict) -> bool:
    alpha = 0.05 # ref val ne pas oublié de mentinné dans le rapport 
    normal:bool =  True
    match cover["type"]:
        case "img":
            image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            pixel_value = image.flatten()
            _,p_value =  shapiro(pixel_value)
            normal = p_value > alpha
        case "son":
            rate, data =  wavfile.read(cover["path"])
            if len(data.shape) > 1:
                data = data.mean(axis=1)
            _,p_value =  shapiro(data)
            normal = p_value > alpha
    return normal

def resitance_a_la_compression(cover:dict):
    psnr:float =  0.0
    match cover["type"]:
        case "img":
            res:float =  0.0
            compression_quality = 50
            image =  cv2.imread(cover["path"])
            cv2.imwrite("to_delete."+cover["path"].split(".")[len(cover["path"].split("."))-1], image, [cv2.IMWRITE_JPEG_QUALITY, compression_quality])
            compressed_image =  cv2.imread("to_delete."+cover["path"].split(".")[len(cover["path"].split("."))-1])

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

            audio.export("to_delete."+cover["path"].split(".")[len(cover["path"].split("."))-1], format=codec, bitrate=bitrate)
            compressed_audio =  AudioSegment.from_file("to_delete."+cover["path"].split(".")[len(cover["path"].split("."))-1])
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

def test_du_khi_carree(cover: dict):
    res = 0
    match cover["type"]:
        case "img":
            image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            hist, _ = np.histogram(image.ravel(), bins=256)
            expected = np.mean(hist)
            chi2_stat, p_val = chi2_contingency([hist, [expected]*256])
            res = 1 if p_val > 0.05 else 0
        case "son":
            _, audio = wavfile.read(cover["path"])
            hist, _ = np.histogram(audio, bins=256)
            expected = np.mean(hist)
            chi2_stat, p_val = chi2_contingency([hist, [expected]*256])
            res = 1 if p_val > 0.05 else 0
    return res

def spectre(cover: dict):
    res = None
    match cover["type"]:
        case "img":
            image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            res = np.abs(fft2(image))
        case "son":
            _, audio = wavfile.read(cover["path"])
            res = np.abs(fft(audio))
    return res

def transformation_en_serie_de_fourier(cover: dict):
    return spectre(cover) 

def transformation_en_ondelette(cover: dict):
    res = None
    match cover["type"]:
        case "img":
            image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            coeffs = wavedec2(image, wavelet='haar', level=2)
            res = coeffs
        case "son":
            _, audio = wavfile.read(cover["path"])
            coeffs = wavedec2(audio.reshape(1, -1), wavelet='haar', level=2)
            res = coeffs
    return res

def la_transformation_de_laplace(cover: dict):
    res = None
    match cover["type"]:
        case "img":
            image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            laplace_transform = cv2.Laplacian(image, cv2.CV_64F)
            res = laplace_transform
        case "son":
            _, audio = wavfile.read(cover["path"])
            laplace_transform = np.gradient(audio)
            res = laplace_transform
    return res

def transformation_en_z(cover: dict):
    res = None
    match cover["type"]:
        case "img":
            image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            z_transform = lapack.dgeev(image.astype(float), compute_vl=False, compute_vr=False)[0]
            res = z_transform
        case "son":
            _, audio = wavfile.read(cover["path"])
            z_transform = lapack.dgeev(audio.astype(float), compute_vl=False, compute_vr=False)[0]
            res = z_transform
    return res

def dct_pour_la_compression(cover: dict):
    res = None
    match cover["type"]:
        case "img":
            image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            dct_image = cv2.dct(image.astype(float))
            res = dct_image
        case "son":
            _, audio = wavfile.read(cover["path"])
            dct_audio = fft(audio)
            res = dct_audio
    return res

def analyse_de_la_densite_spectrale_de_puissance(cover: dict):
    res = None
    match cover["type"]:
        case "img":
            image = cv2.imread(cover["path"], cv2.IMREAD_GRAYSCALE)
            frequencies, power = welch(image.ravel())
            res = {"frequencies": frequencies, "power": power}
        case "son":
            _, audio = wavfile.read(cover["path"])
            frequencies, power = welch(audio)
            res = {"frequencies": frequencies, "power": power}
    return res
