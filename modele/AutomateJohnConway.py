from typing import List
from GameOfLifeException import GameOfLifeException
from controleur import demander_taille_automate, afficher_automate

automate_etat_1 : List[List[str]]
automate_etat_2 : List[List[str]]

def lancer_automate():
    dimensions_automate = demander_taille_automate()
    automate_etat_1 = initialiser_automate(dimensions_automate[0], dimensions_automate[1])
    automate_etat_2 = automate_etat_1
    afficher_automate(automate_etat_1)

# Créer un tableau à deux dimensions, de la taille rentrée en paramètre
# largeur: la largeur du tableau qui sera créé et retourné, accepte un entier > 0 et <100
# hauteur: la hauteur du tableau qui sera créé et retourné, accepte un entier > 0 et <100
def initialiser_automate(largeur: int, hauteur: int) -> List[List[str]]:
    if not isinstance(largeur, int) or not isinstance(hauteur, int):
        raise GameOfLifeException(1, "Paramètres d'initialisation de l'automate incorrects")
    elif largeur < 1 or largeur > 99 or hauteur < 1 or hauteur > 99:
        raise GameOfLifeException(1, "Paramètres d'initialisation de l'automate incorrects")
    else:
        automate_initial = []
        iteration_largeur = 0
        while iteration_largeur < largeur:
            liste_hauteur = []
            iteration_hauteur = 0
            while iteration_hauteur < hauteur:
                liste_hauteur.append("x")
                iteration_hauteur += 1
            automate_initial.append(liste_hauteur)
            iteration_largeur += 1
        return automate_initial
    return None