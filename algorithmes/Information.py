"""

"""

class Information:
    """
    Information (définition inductive): 
        - information_vide  -> (information_vide) | (Est une fomation de taille 0)
        - b in B -> (b) | (est une information de taille 1)
        - On pération +
            - b in B  (b) + (infomation_vide) = (b)
            - pour tout n in N b_0,...b_n in B^n  (b_0) + ... + (b_n) = (b_0, ... , b_n) | (est une infomation de taille n + 1)
        - Une matrice d'information est une information
        - L'ensemble des infomation forme un (B union {information_vide)}-espace vectoriel
    """

    B:set = {0,1}
    EPSILONE:list = [[()]]

    def __init__(self) -> None:
        pass

    def creeinformation() -> None : 
        pass