# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import config
from typing import List

config.configurer_pythonpath()

from controleur import demander_taille_automate, afficher_automate

automate_etat_1 : List[List[str]] = []
automate_etat_2 : List[List[str]] = []

def initialiser_automate(largeur: int, hauteur: int) -> int:

    iteration_largeur = 0
    while iteration_largeur < largeur:
        liste_hauteur = []
        iteration_hauteur = 0
        while iteration_hauteur < hauteur:
            liste_hauteur.append("x")
            iteration_hauteur += 1
        automate_etat_1.append(liste_hauteur)
        iteration_largeur += 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    dimensions_automate = demander_taille_automate()
    initialiser_automate(dimensions_automate[0], dimensions_automate[1])
    afficher_automate(automate_etat_1)

