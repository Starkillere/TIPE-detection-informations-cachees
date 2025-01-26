#-*- encoding:utf-8 -*-

"""Étude des caractèristiques"""

"""main"""

 # IMPORTATIONS DÉPENDENCES

from src import *
import os

 # paramètre globals

db_nom =  "database.db"

 # INITIALISATION

if not os.path.exists(db_nom):
    data_preprocessing.creation_donnees()
    data_preprocessing.create_database(db_nom)
    
    features =  feature_extraction.extract_all_features()
    data_preprocessing.insert_features_into_db(db_nom, features)
