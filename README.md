# TIPE-detection-informations-cachees

## Problématique : Est-il possible de créer un algorithme de stéganalyse géneraliste, i.e un algorithme qui n'a pas connaissance du mode de dissimulation utilisé ?

    - Sous-problèmatique : __Est-il possible d’identifier un invariant de dissimulation, c’est-à-dire une caractéristique commune à toutes les données issues d’un processus de stéganographie, indépendamment de l’algorithme utilisé ou du type de données, permettant ainsi de détecter la présence d’information cachée ?__

- Prototype de l'agorithme :
    entrées : données, type
    sortie : bool -> (true si cache une information, false sinon)

pour la rendre plus compréhensible et meilleur en mettent en avant les point important 

## Sources des données : 
 - source images :  [landscape images](https://www.kaggle.com/datasets/arnaud58)
 - source sons : [Speaker Recognition Audio Dataset](https://www.kaggle.com/datasets/vjcalling/speaker-recognition-audio-dataset)