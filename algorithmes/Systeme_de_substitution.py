"""
    Méthodes de Stéganographie par substitution de bit

    Par : Anrezki Ayouba
    initialisé le : 26/09/2024
    TIPE : 2024-2025 
    MAJ :
"""

from Information import Information
from random import SystemRandom

aleatoirgenerateur = SystemRandom()
#addaptation pour le nombre de bits 
def substitution(hote:Information, information:Information) -> Information: 

    """
        Post-condition : les information sont de même dimension
        Entrees : hote l'image perteuse, image l'image à cahcée
        Sortie : une imaformation 
        Pré-condition : pour chauque élément E_(i,j,k) sont écriture en base 2 sur 8 bits 
                        vaut l'union des quatre premier bits de la décomposition en base 2 sur 8 bits de l'hote et 
                        de la décomposition en base 2 sur 8 bits de l'information (à cachée)
    """

    def remplacer(val_hote:int, val_information:int) -> int:

        """
            fonction auxilière
            entrées : val_hote et val_information deux entiers
            sorties : un entier
            post-condition : l'entier retourner à pour décomposition en base 2 sur 8 bits les quatre premier bits de val_hot
                             et les 4 premier bits de val_information (premier bits -> bits de poid fort)
        """

        bin_val_hote:str = bin(val_hote)[2:]
        bin_val_information:str = bin(val_information)[2:]
        
        octets_hote:str = bin_val_hote+"0"*(8-len(octets_hote))
        octets_information:str = bin_val_information+"0"*(8-len(octets_information))

        octets_nouv_val:str = octets_hote[:4]+octets_information[4:]

        nouv_val:int = int(octets_hote, 2)

        return nouv_val

    assert information.dimension == hote.dimension

    cover:Information = Information(f"{information.nom_information}-hide", f"subsitution", hote.nombre_lignes, hote.nombre_colonnes, hote.taille_uplet)

    for i in range(cover.nombre_lignes):
        for j in range(cover.nombre_colonnes):
            for k in range(cover.taille_uplet):
                cover.forme_matricielle[i][j][k] = remplacer(hote.forme_matricielle[i][j][k], information.forme_matricielle[i][j][k])
    return cover

def cree_cover(information:Information) -> Information:
    
    """
        entrée : information
        sortie : Information 
    """

if __name__ == '__main__':
   

    def random_init(inf:Information) -> Information:
        
        """
        """
        
        for i in range(inf.nombre_lignes):
            for j in range(inf.nombre_colonnes):
                for p in range(inf.taille_uplet):
                    inf.forme_matricielle[i][j][p] = aleatoirgenerateur.randint(0,255)
        return inf
    
    info:Information =  random_init(Information("test-0", "alea-de-la-vie", 500, 500, 3))
    cover_info:Information = random_init(Information("test-0", "alea-de-la-vie", 500, 500, 3))

    print(info)
    print(cover_info)

    