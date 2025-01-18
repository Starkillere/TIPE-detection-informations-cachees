"""

Définition du type information 
Par Ayouba Anrezki
le 10/10/2024

"""
import random
from typing import Callable, Tuple
import numpy as np

__all__ = ["Information"]

class Information:

    """
        Description :
            Information est une définition formelle de la notion d'information
            i.e l'information est reprensenté comme étant une matrice de uplet de bits permetant sa caractérisation
    """

    EPSILONE:list = [[()]]

    def __init__(self, nom_information:str, nom_de_l_algorithme:str, nombre_de_lignes:int, nombre_de_colonnes:int, taille_uplet:int) -> None:
        #Rajouter le codage des nombre i.e sur combien de bit peut se représenter le max 
        self.nom_information:str = nom_information
        self.nom_algorithme:str = nom_de_l_algorithme
        self.nombre_lignes:int = nombre_de_lignes
        self.nombre_colonnes:int = nombre_de_colonnes
        self.taille_uplet:int = taille_uplet
        self.taille:int = self.__calcule_taille()
        self.dimension:int = (self.nombre_lignes, self.nombre_colonnes, self.taille_uplet)
        self.forme_matricielle:list =  self.__init_forme_matricielle()

    
    def __calcule_taille(self) -> int:
        return self.nombre_colonnes*self.nombre_lignes*self.taille_uplet
    
    def __print_forme_matricielle(self) -> str:
        repr:str = str()
        mat:list = self.forme_matricielle
        
        repr = repr+"\n"
        for i in range(self.nombre_lignes):
            repr = repr+"\n[ "
            for j in range(self.nombre_colonnes):
                repr = repr+"\n( "
                for k in range(self.taille_uplet):
                    repr = repr+str(self.forme_matricielle[i][j][k])+" "
                repr = repr+" )\n"
            repr = repr+" ]\n"
        repr = repr+"\n"

        return repr
    
    def __init_forme_matricielle(self) -> list:
        return [[[0 for p in range(self.taille_uplet)] for j in range(self.nombre_colonnes)] for i in range(self.nombre_lignes)]
    
    def __str__(self) -> str:
        return f"""\nInformation : {self.nom_information}\nAlgorithme : {self.nom_algorithme}\nTaille : {self.taille}\nRepresentation matricielle : {self.__print_forme_matricielle()} """
    
    def __repr__(self) -> str:
        return f"""\nInformation : {self.nom_information}\nAlgorithme : {self.nom_algorithme}\nTaille : {self.taille}\nRepresentation matricielle : {self.__print_forme_matricielle()} """
    

class InformationV:
    """
    Représente une information comme une application discrète f : Z^n -> R^m
    et sa matrice associée dans la base canonique de R^m.
    """

    def __init__(self, function: Callable[[Tuple[int, ...]], np.ndarray], shape: Tuple[int, int, int]):
        """
        Initialise l'information.
        
        :param function: Une fonction qui mappe des indices (Z^n) à des valeurs (R^m).
        :param shape: Un tuple (n, l, p) où :
                      - n : Dimension des indices.
                      - l, p : Dimensions spatiales ou temporelles de la matrice.
        """
        self.function = function  # Application discrète f : Z^n -> R^m
        self.shape = shape  # Dimensions de la matrice résultante
        self.matrix = self._generate_matrix()

    def _generate_matrix(self) -> np.ndarray:
        """
        Génère la représentation matricielle de l'information dans la base canonique.

        :return: Une matrice de dimensions (l, p, m) représentant l'application f.
        """
        n, l, p = self.shape
        matrix = np.zeros((l, p, n))
        for i in range(l):
            for j in range(p):
                indices = (i, j)
                matrix[i, j] = self.function(indices)
        return matrix

    def __repr__(self):
        return f"Information(shape={self.shape}, matrix=\n{self.matrix})"
