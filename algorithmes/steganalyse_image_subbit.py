"""
	projet : triangele de trouble
	par : AYOUBA Anrezki
	initialisation : 12/03/2024
	MAJ : 28/05/2024
"""

import numpy as np
from PIL import Image
import datetime
import random
 
randomSys = random.SystemRandom()

def generateurImageAleatoir(size:tuple[int, int]) -> str:
	"""
		entrees : size tuple d'entiers naturels (dimmension de l'image)
		pré-conditions : size = (x, y) in  NN^2
		sorties : nom (nom donné à l'image géneré)
		post-conditions : non est un e chaine de carractères correspondant à la date de géneration de l'image.
	"""
	matrice = np.array([[[np.uint8(randomSys.randint(0, 255)) for k in range(3)] for j in range(size[1])] for i in range(size[0])])
	image =  Image.fromarray(matrice)
	nom = datetime.datetime.now()
	image.save(f"{nom}.png")
	return  f"{nom}.png"

def generateurRectangle(image:str) -> tuple[float, float]:
	"""
		entrees : image une chaine de carractére.
		pré-condition : image indique le nom  du fichier image format png dans le répertoir courant du fichier contenant ce programme.
		sorties : rectangle tuple de réel positifs  (dimension du rectangle)
		post-conditions :  rectangle = (x,y) in  RR^2+.
	"""
	matrice_image = np.array(Image.open(image))
	dim_matrice_image = (len(matrice_image[0]), len(matrice_image))
	rectangle = (int(dim_matrice_image[0]/2),int(dim_matrice_image[1]/2))
	return rectangle


def estHomogene(rectangle:tuple[float, float], image:str, seuil:int=20) -> bool:
 
    """
    entrees : rectange (dimension du rectangle), image (nom  du fichier image format png), seuil (valeur de seuil de différence de couleur)
    pré-condition : rectangle = (x,y) in  RR^2+., 
    sorties : homogene image indique le nom  du fichier image format png dans le répertoir courant du fichier contenant ce programme.
    post-conditions : True si l'image est homogène, False sinon
    """

    # Ouvrir l'image
    image = Image.open(image)
    matrice = np.array(image)

    # Diviser l'image en zones basées sur le rectangle donné
    x, y = rectangle
    nb_col = matrice.shape[1] // x
    nb_lignes = matrice.shape[0] // y

    # Calculer la moyenne des valeurs de couleur pour chaque zone
    moyennes = []
    for i in range(nb_lignes):
        for j in range(nb_col):
            zone = matrice[i*y:(i+1)*y, j*x:(j+1)*x]
            moyenne_zone = np.mean(zone, axis=(0, 1))
            moyennes.append(moyenne_zone)

    # Vérifier l'homogénéité en comparant les moyennes de chaque zone
    for i in range(len(moyennes)-1):
        for j in range(i+1, len(moyennes)):
            difference = np.linalg.norm(moyennes[i] - moyennes[j])
            if difference > seuil:
                return False

    return True

def recup_image_cachee(img:str) -> str:

    """
        entrees : img (chaine de carractères)
            pré-conditons: le chemin doit être correct
        sorties : image_cachee (chaine de carractères)
            post-conditions : image_cachee correspond à l'image formet par les bits de poid faible de l'image hote
    """

    image =  Image.open(img)
    mat =  np.array(image)
    taille = (len(mat), len(mat[0]))

    image_cachee = []

    for i in range(taille[0]):
        colonne = []
        for j in range(taille[1]):
            pixel = []
            for p in range(3):
                elmt = bin(mat[i][j][p])[2:]
                elmt = ((8-len(elmt))*"0"+elmt)[4:]+"0"*4
                pixel.append(np.uint8(int(elmt,2)))
            colonne.append(pixel)
        image_cachee.append(colonne)
    
    image_cachee = np.array(image_cachee)

    image =  Image.fromarray(image_cachee)

    nom = datetime.datetime.now()
    image.save(f"{nom}.png")
    return  f"{nom}.png"

def cacher_dans_poid_faible(image_a_cacher:str, image_hote:str) -> str:

    """

    """

    image_a_cacher =  Image.open(image_a_cacher)
    mat_hote =  np.array(Image.open(image_hote).resize(image_a_cacher.size))
    mat_image_a_cacher = np.array(image_a_cacher)


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
    
    mat_steg =  np.array(ligne)
    image_steg =  Image.fromarray(mat_steg)
    nom = datetime.datetime.now()
    image_steg.save(f"{nom}.png")
    return  f"{nom}.png"
if __name__ == "__main__" :
    estHomogene()
