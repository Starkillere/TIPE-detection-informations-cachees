#-*- encoding:utf-8 -*-

"""traitement des données"""

"""Par Ayouba Anrezki """

 # IMPORTATIONS DÉPENDENCES

from PIL import Image
import numpy as np
from scipy.io import wavfile
import faker
import os
import sqlite3
import shutil

__all__ =  ["creation_donnees", "create_database", "insert_features_into_db"]

 # paramètre globals

longueur_max_message = 50 # en nombre de caractère
dir_data =  "data/raw/"
dir_clean =  "data/clean/"
dir_stego =  "data/stego/"

 # CLASSIFICATION stego/clean



     # Algorithms de dissimulation (lsb pour les image images)/mpa les audios)) sur du text

def lsb(input_file:str, output_file:str, message) -> None:
    assert input_file.split(".")[-1] == "jpg"
    assert output_file.split(".")[-1] == "jpg"

    img = Image.open(input_file)
    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '1111111111111110'
    img_data = list(img.getdata())
    if len(binary_message) > len(img_data) * 3:
        raise ValueError("Message too large to hide in image.")

    new_data = []
    binary_idx = 0

    for pixel in img_data:
        r, g, b = pixel[:3]
        if binary_idx < len(binary_message):
            r = (r & ~1) | int(binary_message[binary_idx])
            binary_idx += 1
        if binary_idx < len(binary_message):
            g = (g & ~1) | int(binary_message[binary_idx])
            binary_idx += 1
        if binary_idx < len(binary_message):
            b = (b & ~1) | int(binary_message[binary_idx])
            binary_idx += 1
        new_data.append((r, g, b) + pixel[3:] if len(pixel) == 4 else (r, g, b))

    img.putdata(new_data)
    img.save(output_file)

def mpa(input_file:str, output_file:str, message) -> None:
    assert input_file.split(".")[-1] == "wav"
    assert output_file.split(".")[-1] == "wav"

    rate, data = wavfile.read(input_file)
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '11111110'
    message_bits = list(map(int, binary_message))
    flat_data = data.flatten()
    if len(message_bits) > len(flat_data):
        raise ValueError("Message too large for audio.")
    
    for i, bit in enumerate(message_bits):
        flat_data[i] = (flat_data[i] & ~1) | bit

    new_data = flat_data.reshape(data.shape)
    wavfile.write(output_file, rate, new_data.astype(data.dtype))

    # Création des données (stego / clean)

def creation_donnees() -> None:

    fichiers = [f for f in os.listdir(dir_data) if os.path.isfile(os.path.join(dir_data, f))]
    images =  [img for img in fichiers if img.split(".")[-1] == "jpg"]
    audios =  [aud for aud in fichiers if aud.split(".")[-1] == "jpg"]

    stegos =  images[:(len(images)//2)] + audios[:(len(audios)//2)]
    cleans =  images[(len(images)//2):] + audios[(len(audios)//2):]
    fk =  faker.Faker()
    messages = [fk.text(max_nb_chars=longueur_max_message) for i in range(len(stegos))]

     # sauvegarder clean

    for fichier in cleans:
        source_path = os.path.join(dir_data, fichier)
        dest_path = os.path.join(dir_clean, fichier)
        shutil.copy(source_path, dest_path)
    
     # creation stego et sauvegarde

    for stego in stegos:
        if stego.split(".")[-1] == "jpg":
            lsb(f"{dir_data}{stego}", f"{dir_stego}{stego}", messages[stegos.index(stego)])
        else:
            mpa(f"{dir_data}{stego}", f"{dir_stego}{stego}", messages[stegos.index(stego)])

# base de données

  # creation de la base de données

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_size INTEGER,
            entropy REAL,
            zero_density REAL,
            one_density REAL,
            mean_value REAL,
            std_dev REAL,
            energy REAL,
            variance REAL,
            is_stego INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Base de données créée ou existante à : {db_path}")

    # Insertion des caracteristiques

def insert_features_into_db(db_path, features):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for feature in features:
        cursor.execute('''
            INSERT INTO features (
                file_size, entropy, zero_density, one_density, 
                mean_value, std_dev, energy, variance, is_stego
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            feature["file_size"],
            feature["entropy"],
            feature["zero_density"],
            feature["one_density"],
            feature["mean_value"],
            feature["std_dev"],
            feature["energy"],
            feature["variance"],
            feature["is_stego"]
        ))
        print(f"Données insérées : {features}")
    conn.commit()
    conn.close()