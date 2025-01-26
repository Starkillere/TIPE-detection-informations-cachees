# TIPE-detection-informations-cachees

## Problématique : Est-il possible de détecter des informations cachées dans des fichiers JPG sans connaître la méthode de dissimulation utilisée ?

    - Sous-problématique : __Est-il possible d’identifier un invariant de dissimulation, c’est-à-dire une caractéristique commune à toutes les données issues d’un processus de stéganographie, indépendamment de l’algorithme utilisé ou du type de données, permettant ainsi de détecter la présence d’information cachée dans des images JPG ?__

- Prototype de l'algorithme :
    Entrées : image (fichier JPG), méthode de dissimulation (non nécessaire)
    Sortie : booléen -> (true si l'image cache une information, false sinon)

## Sources des données :
- **Source d'images** : [Kaggle Landscape Images Dataset](https://www.kaggle.com/datasets/arnaud58) 
- **Source de données pour l'entraînement** : [Speaker Recognition Audio Dataset](https://www.kaggle.com/datasets/vjcalling/speaker-recognition-audio-dataset)

## Objectifs :
Le projet se concentre sur la détection d’informations cachées dans des images JPG en recherchant un invariant qui soit indépendant de la méthode de dissimulation utilisée. L'objectif est de concevoir un algorithme capable d'analyser des fichiers JPG et de détecter la présence d'information cachée sans connaître préalablement la méthode de stéganographie employée.

## Méthodes utilisées :
- **LSB (Least Significant Bit)** : Utilisé pour l'insertion de données dans les bits les moins significatifs des pixels d'une image.
- **Codage de pixels** : Techniques qui manipulent les valeurs des pixels de manière systématique pour y intégrer des données cachées.
- **Masquage dans les Zones Inutilisées (ROI)** : Exploitation des parties de l’image où les modifications passent inaperçues.
- **Stéganographie par palette de couleurs** : Utilisation de la palette de couleurs dans les images pour dissimuler des informations.

## Prochaines étapes :
- Collecte d'images et prétraitement des données.
- Développement d'un modèle pour identifier les invariants dans les images.
- Tests et validation sur un ensemble d'images stégo et clean.
