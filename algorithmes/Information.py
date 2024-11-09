"""

Définition du type information 
Par Ayouba Anrezki
le 10/10/2024

"""
import random

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
        self.nom_information:str =  nom_information
        self.nom_algorithme:str = nom_de_l_algorithme
        self.nombre_lignes:int = nombre_de_lignes
        self.nombre_colonnes:int = nombre_de_colonnes
        self.taille_uplet:int = taille_uplet
        self.taille:int = self.__calcule_taille()
        self.dimension:int = (self.nombre_lignes, self.nombre_colonnes, self.taille_uplet)
        self.forme_matricielle:list =  self.__init_forme_matricielle()

    

    def __calcule_taille(self) -> int:
        return self.nombre_colonnes*self.nombre_lignes*self.taille_uplet
    
    def __init_forme_matricielle(self) -> list:
        return [[[0 for p in range(self.taille_uplet)] for j in range(self.nombre_colonnes)] for i in range(self.nombre_lignes)]
    
    def __str__(self) -> str:
        return f"""\nInformation : {self.nom_information}\nAlgorithme : {self.nom_algorithme}\nTaille : {self.taille}\nRepresentation matricielle : """
    
    def __repr__(self) -> str:
        return f"""\nInformation : {self.nom_information}\nAlgorithme : {self.nom_algorithme}\nTaille : {self.taille}\nRepresentation matricielle : """
