import sqlite3 
import faker
import random
import os 

#Note a moi même : faire une étude de donnée non stéganographie et en suite lancé un algortheme de classification 
def hote_loader(database: str):
    """
    Charge les données des hôtes à partir du dossier "hotes" et les insère dans la base de données.
    """
    dir_name = "hotes"
    filenames = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))]
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    for filename in filenames:
        path = os.path.join(dir_name, filename)
        hote_type = "img" if filename.split(".")[-1] == "jpg" else "son"
        methode = "mpa" if hote_type == "son" else random.choice(["lsb", "dtc"])
        
        taille = os.path.getsize(path)

        cursor.execute("""
            INSERT INTO hote_data (path, type, methode, taille, Note) 
            VALUES (?, ?, ?, ?, ?)
        """, (path, hote_type, methode, taille, None))
    
    conn.commit()
    conn.close()

def hide_loader(database: str):
    """
    Génère des données aléatoires à cacher et les insère dans la base de données.
    """
    fk = faker.Faker()
    hides = []

    max_count = len([f for f in os.listdir("hotes") if os.path.isfile(os.path.join("hotes", f))])
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    for i in range(1, max_count + 1): 
        content = fk.text(max_nb_chars=50)
        taille = len(content.encode("utf-8")) 
        id_hoteData = i 
        
        cursor.execute("""
            INSERT INTO hide_data (content, type, id_hoteData, taille, Note) 
            VALUES (?, ?, ?, ?, ?)
        """, (content, "texte", id_hoteData, taille, None))
    
    conn.commit()
    conn.close()
