#-*- encoding:utf-8 -*-

"""Étude des caractèristiques"""

"""main"""

 # IMPORTATIONS DÉPENDENCES

import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
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


 # PREMIERE APPROCHE VERS UN PARTITIONNEMENT ET AFFICAHGE DES DONNÉES

def load_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM features"
    df = pd.read_sql_query(query, conn)
    conn.close()

    X = df.drop(columns=["id", "is_stego"]) 
    y = df["is_stego"] 
    return X, y

def cluster_and_visualize(X, y):
    """
    Applique le clustering sur les données et affiche les résultats sur un graphique.
    :param X: Caractéristiques
    :param y: Étiquettes réelles (pour comparaison)
    """
    
    pca = PCA(n_components=2)  
    X_pca = pca.fit_transform(X)

    kmeans = KMeans(n_clusters=2, random_state=42)
    clusters = kmeans.fit_predict(X)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)

    axes[0].scatter(
        X_pca[:, 0], X_pca[:, 1],
        c=y, cmap="bwr", alpha=0.6, edgecolor='k'
    )
    axes[0].set_title("Données réelles : Stégo vs Non-Stégo")
    axes[0].set_xlabel("Composante principale 1")
    axes[0].set_ylabel("Composante principale 2")
    axes[0].legend(handles=[
        plt.Line2D([0], [0], marker='o', color='w', label='Non-Stégo', markersize=10, markerfacecolor='blue'),
        plt.Line2D([0], [0], marker='o', color='w', label='Stégo', markersize=10, markerfacecolor='red')
    ])

    axes[1].scatter(
        X_pca[:, 0], X_pca[:, 1],
        c=clusters, cmap="viridis", alpha=0.6, edgecolor='k'
    )
    axes[1].set_title("Résultat du Clustering (K-Means)")
    axes[1].set_xlabel("Composante principale 1")
    axes[1].set_ylabel("Composante principale 2")
    axes[1].legend(handles=[
        plt.Line2D([0], [0], marker='o', color='w', label='Cluster 1', markersize=10, markerfacecolor='yellow'),
        plt.Line2D([0], [0], marker='o', color='w', label='Cluster 2', markersize=10, markerfacecolor='green')
    ])

    plt.tight_layout()
    plt.show()

    agreement = max(np.mean(clusters == y), np.mean(clusters != y))
    print(f"Taux d'accord avec les étiquettes réelles : {agreement * 100:.2f}%")

if __name__ == "__main__":
    DB_PATH = "database.db" 

    X, y = load_data_from_db(DB_PATH)

    cluster_and_visualize(X, y)
