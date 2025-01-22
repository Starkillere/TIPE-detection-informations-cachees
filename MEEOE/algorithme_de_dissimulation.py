import sqlite3 as s3
from Methodes import *
from datetime import datetime

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


def creat_covers(database: str) -> bool:
    """
    Crée les fichiers de couverture à partir des données cachées et des hôtes dans la base de données.
    """
    try:
        hides = collect_hide_data_from_db(database)
        hotes = collect_hote_data_from_db(database)

        for hide in hides:
            hote = next((h for h in hotes if h["id"] == hide["id_hoteData"]), None)
            if not hote:
                print(f"Aucun hôte correspondant trouvé pour hide ID {hide['id']}")
                continue

            methode = hote["methode"]
            output_name = f"covers/cover_{datetime.now().strftime('%Y%m%d%H%M%S')}."+hote["path"].split(".")[len(hote["path"].split("."))-1]
            cover = {"path": output_name, "type": hote["type"], "idhideData": hide["id"]}

            try:
                match methode:
                    case "lsb":
                        lsb.hide_message_lsb(hote["path"], hide["content"], output_name)
                    case "dtc":
                        dtc.hide_message_dct(hote["path"], hide["content"], output_name)
                    case "mpa":
                        mpa.hide_message_audio(hote["path"], hide["content"], output_name)
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
