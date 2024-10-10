"""

Définition du type information 
Par Ayouba Anrezki
le 10/10/2024

"""

class Information:

    EPSILONE:list = [[()]]

    def __init__(self, nom_information:str, nom_de_l_algorithme:str, nombre_de_lignes:int, nombre_de_colonnes:int, taille_uplet:int) -> None:
        self.nom_information =  nom_information
        self.nom_algorithme = nom_de_l_algorithme
        self.nombre_lignes = nombre_de_lignes
        self.nombre_colonnes = nombre_de_colonnes
        self.taille_uplet = taille_uplet
        self.taille = self.__calcule_taille()
        self.forme_matricielle =  self.__init_forme_matricielle()

    def __calcule_taille(self) -> int:
        return self.nombre_colonnes*self.nombre_lignes*self.taille_uplet
    
    def __init_forme_matricielle(self) -> list:
        return [[tuple([0 for p in range(self.taille_uplet)]) for j in range(self.nombre_colonnes)] for i in range(self.nombre_lignes)]