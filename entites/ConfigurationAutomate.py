import json
from typing import List, Dict
class ConfigurationAutomate(object):

    def __init__(self, identifiant: int, nom: str, largeur: int, hauteur: int):
        self.identifiant = identifiant
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur

    def __str__(self):
        return json.dumps({"Identifiant":self.identifiant, "Nom":self.nom, "Largeur":self.largeur, "Hauteur": self.hauteur}, separators=(',', ':'))

    # renvoie un dictionnaire contenant les paramètres de la configuration
    def dictionnaireParametresConfiguration(self) -> Dict:
        return {"Identifiant": self.identifiant, "Nom": self.nom, "Largeur":self.largeur, "Hauteur":self.hauteur}

    @property
    def identifiant(self):
        return self.__identifiant

    @property
    def nom(self):
        return self.__nom

    @property
    def hauteur(self):
        return self.__hauteur

    @property
    def largeur(self):
        return self.__largeur

    @identifiant.setter
    def identifiant(self, identifiant: int):
        if not isinstance(identifiant, int):
            raise ValueError("L'identifiant de la configuration de l'automate n'est pas un entier")
        elif identifiant < 0 or identifiant > 20:
            raise ValueError("L'identifiant de de la configuration de l'automate n'est pas des bornes autorisées (0-19)")
        else:
            self.__identifiant = identifiant

    @nom.setter
    def nom(self, nom: str):
        if not isinstance(nom, str):
            raise ValueError("Le nom de la configuration de l'automate n'est pas une chaine de caractère")
        elif len(nom) > 31:
            raise ValueError("Le nom de de la configuration de l'automate n'est pas de la taille autorisée (1-30)")
        else:
            self.__nom = nom

    @hauteur.setter
    def hauteur(self, hauteur:int):
        if not isinstance(hauteur, int):
            raise ValueError("La hauteur de la configuration de l'automate n'est pas un entier")
        elif hauteur <1 or hauteur > 99:
            raise ValueError("La hauteur de la configuration l'automate n'est pas dans les bornes valides. (Bornes valides: [1;99]")
        else:
            self.__hauteur = hauteur

    @largeur.setter
    def largeur(self, largeur: int):
        if not isinstance(largeur, int):
            raise ValueError("La largeur de la configuration de l'automate n'est pas un entier")
        elif largeur < 1 or largeur > 99:
            raise ValueError("La largeur de la configuration l'automate n'est pas dans les bornes valides. (Bornes valides: [1;99]")
        else:
            self.__largeur = largeur
