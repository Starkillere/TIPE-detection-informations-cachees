import os
import sqlite3 as s3
from datetime import datetime
import numpy as np
import cv2
from scipy.fft import fft, ifft
from pydub import AudioSegment
from stegano import lsb


def collect_hide_data_from_db(database: str) -> list[dict]:
    """
    Collecte les données cachées depuis la base de données.
    """
    hides = []
    try:
        conn = s3.connect(database)
        cursor = conn.cursor()
        query = "SELECT id, content, type, id_hoteData, taille FROM hide_data"
        for row in cursor.execute(query):
            hides.append({
                "id": row[0],
                "content": row[1],
                "type": row[2],
                "id_hoteData": row[3],
                "taille": row[4],
            })
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la collecte des données cachées: {e}")
    return hides


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


def add_cover_data_from_db(database: str, cover: dict) -> bool:
    """
    Ajoute une entrée de donnée de couverture dans la base de données.
    """
    try:
        conn = s3.connect(database)
        cursor = conn.cursor()
        query = """
        INSERT INTO cover_data (path, type, id_hideDat)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (cover["path"], cover["type"], cover["idhideData"]))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de la donnée de couverture: {e}")
        return False


def hide_message_lsb(image_path: str, message: str, output_path: str):
    """Cache un message dans une image au format JPG en utilisant la méthode LSB."""
    secret_image = lsb.hide(image_path, message)
    secret_image.save(output_path)

def hide_message_dct(image_path, message, output_path):
    # Lire l'image et la convertir en niveaux de gris
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"L'image à {image_path} est introuvable ou invalide.")
    
    # Convertir l'image en float32 avant de procéder à la DCT
    image = image.astype(np.float32)

    # Effectuer la transformée en cosinus discrète (DCT)
    dct_image = cv2.dct(image)
    
    # Convertir le message en binaire
    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '11111110'
    binary_idx = 0
    
    # Modifier les coefficients DCT pour cacher le message
    for i in range(dct_image.shape[0]):
        for j in range(dct_image.shape[1]):
            if binary_idx >= len(binary_message):
                break
            # Convertir les coefficients DCT en entiers avant de manipuler les bits
            dct_image[i, j] = (dct_image[i, j] & ~1) | int(binary_message[binary_idx])
            binary_idx += 1
        if binary_idx >= len(binary_message):
            break

    # Recomposer l'image après modification
    modified_image = cv2.idct(dct_image)

def hide_message_audio(audio_path: str, message: str, output_path: str):
    """Cache un message dans un fichier audio WAV."""
    audio = AudioSegment.from_wav(audio_path)
    samples = np.array(audio.get_array_of_samples())

    # Vérification si le message peut être caché
    if len(message) * 8 > len(samples):
        raise ValueError("Le message est trop long pour ce fichier audio.")

    # Conversion du message en binaire
    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '11111110'
    binary_idx = 0

    # Insertion des bits dans les échantillons audio
    for i in range(len(samples)):
        if binary_idx >= len(binary_message):
            break
        samples[i] = (samples[i] & ~1) | int(binary_message[binary_idx])
        binary_idx += 1

    # Sauvegarde du fichier audio modifié
    modified_audio = audio._spawn(samples.tobytes())
    modified_audio.export(output_path, format="wav")

def creat_covers(database: str) -> bool:
    """
    Crée les fichiers de couverture à partir des données cachées et des hôtes dans la base de données.
    """
    try:
        hides = collect_hide_data_from_db(database)
        hotes = collect_hote_data_from_db(database)
        count = 0
        for hide in hides:
            hote = next((h for h in hotes if h["id"] == hide["id_hoteData"]), None)
            if not hote:
                print(f"Aucun hôte correspondant trouvé pour hide ID {hide['id']}")
                continue

            methode = hote["methode"]
            output_name = f"covers/cover_{count}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{hote['path'].split('.')[-1]}"
            cover = {"path": output_name, "type": hote["type"], "idhideData": hide["id"]}
            count += 1
            try:
                match methode:
                    case "lsb":
                        hide_message_lsb(hote["path"], hide["content"], output_name)
                    case "dtc":
                        hide_message_lsb(hote["path"], hide["content"], output_name)
                    case "mpa":
                        hide_message_audio(hote["path"], hide["content"], output_name)
                    case _:
                        print(f"Méthode inconnue : {methode}")
                        continue

                # Ajout de la donnée cover dans la base de données
                if not add_cover_data_from_db(database, cover):
                    print(f"Erreur lors de l'ajout du fichier de couverture : {cover['path']}")
            except Exception as e:
                print(f"Erreur lors de la création de la couverture avec méthode {methode}: {e}")
                continue

    except Exception as e:
        print(f"Erreur lors de la création des couvertures : {e}")
        return False
    return True
