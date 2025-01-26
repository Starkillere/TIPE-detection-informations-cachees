#-*- encoding:utf-8 -*-

"""traitement des données"""

"""Par Ayouba Anrezki """

 # IMPORTATIONS DÉPENDENCES

from PIL import Image
import numpy as np
import random
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


def lsb_text(input_file:str, output_file:str, message) -> None:
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

def lsb_image(input_file:str, output_file:str):
    assert input_file.split(".")[-1] == "jpg"
    assert output_file.split(".")[-1] == "jpg"

    mat_hote =  np.array(Image.open(input_file))
    mat_image_a_cacher =  np.random.randint(0, 256, (len(mat_hote), len(mat_hote[0]), 3), dtype=np.uint8)

    ligne =  list()
    for i in range(len(mat_image_a_cacher)):
        colonne = list()
        for j in range(len(mat_image_a_cacher[0])):
            pixel =  list()
            for p in range(3):

                bit_hote = (bin(mat_hote[i][j][p])[2:])
                bit_hote = ((8-len(bit_hote))*"0"+bit_hote)[:4]

                bit_cache = (bin(mat_image_a_cacher[i][j][p])[2:])
                bit_cache = ((8-len(bit_cache))*"0"+bit_cache)[:4]

                bit =  bit_hote+bit_cache
                
                int_bit =  np.uint8(int(bit,2))

                pixel.append(int_bit)
            colonne.append(tuple(pixel))
        ligne.append(colonne)
    
    img = np.array(ligne)
    img =  Image.fromarray(img)
    img.save(output_file)

def codage_pixels(input_file: str, output_file: str, message: str):
    assert input_file.split(".")[-1].lower() == "jpg"
    assert output_file.split(".")[-1].lower() == "jpg"

    image = Image.open(input_file)
    image = np.array(image)

    message_bin = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'

    max_bits = image.size * 3
    assert len(message_bin) <= max_bits, "Le message est trop long pour être dissimulé dans l'image."

    flat_image = image.flatten()
    for i, bit in enumerate(message_bin):
        flat_image[i] = (flat_image[i] & 254) | int(bit)

    encoded_image = flat_image.reshape(image.shape)
    encoded_image = Image.fromarray(encoded_image)
    encoded_image.save(output_file)

def palette_de_couleur(input_file: str, output_file: str, message: str):
    assert input_file.split(".")[-1].lower() == "jpg"
    assert output_file.split(".")[-1].lower() == "jpg"

    image = Image.open(input_file).convert("RGB")
    image_array = np.array(image)

    message_bin = ''.join(format(ord(c), '08b') for c in message)
    message_values = [int(message_bin[i:i+8], 2) for i in range(0, len(message_bin), 8)]

    transformed_image = image_array.copy()
    for i, value in enumerate(message_values):
        transformed_image[..., i % 3] = np.uint8(transformed_image[..., i % 3] + value)


    transformed_image_pil = Image.fromarray(transformed_image)
    transformed_image_pil.save(output_file)



    # Création des données (stego / clean)

def creation_donnees() -> None:

    fichiers = [f for f in os.listdir(dir_data) if os.path.isfile(os.path.join(dir_data, f))]
    images =  [img for img in fichiers if img.split(".")[-1] == "jpg"]
    audios =  [aud for aud in fichiers if aud.split(".")[-1] == "jpg"]

    stegos =  images[:(len(images)//2)] + audios[:(len(audios)//2)]
    cleans =  images[(len(images)//2):] + audios[(len(audios)//2):]
    fk =  faker.Faker()

     # sauvegarder clean

    for fichier in cleans:
        source_path = os.path.join(dir_data, fichier)
        dest_path = os.path.join(dir_clean, fichier)
        shutil.copy(source_path, dest_path)
    
    for stego in stegos:

        match random.choice([0,1,2,3]):
            case 0:
                message =  fk.text(max_nb_chars=longueur_max_message)
                lsb_text(f"{dir_data}{stego}", f"{dir_stego}{stego}", message)
            case 1:
                lsb_image(f"{dir_data}{stego}", f"{dir_stego}{stego}")
            case 2:
                message =  fk.text(max_nb_chars=longueur_max_message)
                codage_pixels(f"{dir_data}{stego}", f"{dir_stego}{stego}", message)
            case 3:
                message =  fk.text(max_nb_chars=longueur_max_message)
                palette_de_couleur(f"{dir_data}{stego}", f"{dir_stego}{stego}", message)
    
     # creation stego et sauvegarde

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
            khi2 REAL,
            vraisemblance REAL,
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
                mean_value, std_dev, energy, variance, khi2, vraisemblance, is_stego
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            feature["file_size"],
            feature["entropy"],
            feature["zero_density"],
            feature["one_density"],
            feature["mean_value"],
            feature["std_dev"],
            feature["energy"],
            feature["variance"],
            feature["khi2"],
            feature["vraisemblance"],
            feature["is_stego"]
        ))
        print(f"Données insérées : {features}")
    conn.commit()
    conn.close()